import os
import tempfile
import shutil
import numpy as np
import pytest
from edgedemo.detection import ImageLoader, PeopleDetector

class DummyYOLO:
    """A dummy YOLO model for testing PeopleDetector without actual model files."""
    def __init__(self, *args, **kwargs):
        pass

    def predict(self, img):
        class DummyBox:
            def __init__(self):
                self.cls = np.array([0])
                self.xyxy = np.array([[10, 10, 50, 50]])
        class DummyResult:
            def __init__(self):
                self.boxes = [DummyBox()]
                self.names = {0: "person", 1: "cat"}
        return [DummyResult()]

@pytest.fixture
def image_dir_with_images():
    temp_dir = tempfile.mkdtemp()
    img1 = np.ones((100, 100, 3), dtype=np.uint8) * 255
    img2 = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2 = __import__("cv2")
    cv2.imwrite(os.path.join(temp_dir, "img1.jpg"), img1)
    cv2.imwrite(os.path.join(temp_dir, "img2.png"), img2)
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_generate_frames_from_directory(image_dir_with_images):
    loader = ImageLoader(image_dir_with_images, realtime=False)
    frames = list(loader.generate_frames())
    assert len(frames) == 2
    assert all(isinstance(f, np.ndarray) for f in frames)

def test_generate_frames_invalid_image(tmp_path, caplog):
    # Create a fake image file that can't be loaded
    bad_img_path = tmp_path / "bad.jpg"
    bad_img_path.write_bytes(b"not an image")
    loader = ImageLoader(str(tmp_path), realtime=False)
    frames = list(loader.generate_frames())
    assert frames == []
    assert "Could not load image" in caplog.text

def test_load_image_success(image_dir_with_images):
    loader = ImageLoader(image_dir_with_images)
    img_path = os.path.join(image_dir_with_images, "img1.jpg")
    img = loader._load_image(img_path)
    assert isinstance(img, np.ndarray)

def test_load_image_failure(tmp_path):
    loader = ImageLoader(str(tmp_path))
    with pytest.raises(ValueError):
        loader._load_image(str(tmp_path / "nonexistent.jpg"))

def test_people_detector_detect(monkeypatch, image_dir_with_images):
    # Patch YOLO in PeopleDetector to use DummyYOLO
    monkeypatch.setattr("edgedemo.detection.YOLO", DummyYOLO)
    loader = ImageLoader(image_dir_with_images, realtime=False)
    detector = PeopleDetector()
    count, crops = detector.detect(loader, number_of_images=2)
    assert count == 2  # 1 person per image, 2 images
    assert len(crops) == 2
    assert all(isinstance(c, np.ndarray) for c in crops)

def test_people_detector_no_people(monkeypatch, image_dir_with_images):
    class NoPersonYOLO:
        def __init__(self, *a, **k): pass
        def predict(self, img):
            class DummyBox: 
                def __init__(self): self.cls = np.array([1]); self.xyxy = np.array([[0,0,1,1]])
            class DummyResult:
                def __init__(self): self.boxes = [DummyBox()]; self.names = {0: "person", 1: "cat"}
            return [DummyResult()]
    monkeypatch.setattr("edgedemo.detection.YOLO", NoPersonYOLO)
    loader = ImageLoader(image_dir_with_images, realtime=False)
    detector = PeopleDetector()
    count, crops = detector.detect(loader, number_of_images=2)
    assert count == 0
    assert crops == []

def test_people_detector_empty_dir(monkeypatch, tmp_path):
    monkeypatch.setattr("edgedemo.detection.YOLO", DummyYOLO)
    loader = ImageLoader(str(tmp_path), realtime=False)
    detector = PeopleDetector()
    count, crops = detector.detect(loader, number_of_images=2)
    assert count == 0
    assert crops == []