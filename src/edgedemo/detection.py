
import cv2
import sys
import os
import logging
from ultralytics import YOLO
from typing import Tuple, List, TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
from tqdm import tqdm

_logger = logging.getLogger(__name__)

class ImageLoader:
    def __init__(self, image_path: str, realtime: bool = False):
        self._image_path = image_path
        self._realtime = realtime

    def generate_frames(self, number_of_images: int = 4) -> "Iterator[np.ndarray]":
        """
        Generates image frames either from a directory of images or from a live camera feed.

        If realtime mode is disabled, iterates over image files in the specified directory,
        loading each image and yielding it as a frame. Only files with '.jpg' or '.png'
        extensions are considered. If an image fails to load, an error is logged and the
        method continues with the next image.

        If realtime mode is enabled, captures frames from the default camera device.
        Yields the specified number of frames captured from the camera. If a frame cannot
        be captured, a message is printed and the method continues.

        Args:
            number_of_images (int, optional): Number of frames to capture from the camera
                when in realtime mode. Defaults to 1.

        Yields:
            np.ndarray: The next image frame, either loaded from disk or captured from
                the camera.

        Raises:
            ValueError: If an image file cannot be loaded (handled internally and logged).
        """
        if not self._realtime:
            image_files = [img for img in os.listdir(self._image_path) if img.endswith('.jpg') or img.endswith('.png')]
            if not image_files:
                _logger.warning("No image files found in directory: %s", self._image_path)
                sys.exit(1)
            for image in tqdm(image_files, desc="Loading images"):
                full_path = os.path.join(self._image_path, image)
                try:
                    frame = self._load_image(full_path)
                except ValueError as e:
                    _logger.error("Could not load image %s: %s", full_path, e)
                    continue
                yield frame
        else:
            cap = cv2.VideoCapture(0)
            for _ in range(number_of_images):
                ret, frame = cap.read()
                if ret:
                    yield frame
                else:
                    print("Failed to capture camera frame.")
            cap.release()

    def _load_image(self, path: str) -> "np.ndarray":
        image = cv2.imread(path)
        if image is None:
            raise ValueError(f"Image not found or unable to load: {path}")
        return image

class PeopleDetector:
    def __init__(self, model_path: str = "yolov8s.pt"):
        self.model = YOLO(model_path)
        self.crops: List["np.ndarray"] = []
        self.people_counter: int = 0

    def detect(
        self,
        loader: "ImageLoader",
        number_of_images: int = 3
    ) -> Tuple[int, List["np.ndarray"]]:
        """
        Detects people in images provided by a loader, crops their bounding boxes, and counts the number of detected people.

        Args:
            loader: An object with a `generate_frames(number_of_images)` method that yields images to process.
            number_of_images (int, optional): The number of images to process from the loader. Defaults to 3.

        Returns:
            tuple: A tuple containing:
                - people_counter (int): The total number of detected people across all processed images.
                - crops (list): A list of cropped image regions corresponding to detected people.
        """
        self.crops = []
        self.people_counter = 0
        for img in loader.generate_frames(number_of_images=number_of_images):
            results = self.model.predict(img)
            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    if result.names[cls_id] == "person":
          
                        self.people_counter += 1
                        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                        cropped = img[y1:y2, x1:x2]
                        self.crops.append(cropped)
        return self.people_counter, self.crops

