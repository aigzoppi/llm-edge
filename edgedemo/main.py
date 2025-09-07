###################################################################

# Step 2: Import the YOLO class
from ultralytics import YOLO
import cv2 # cv2 is OpenCV, a library for image processing
from google.colab.patches import cv2_imshow # cv2_imshow is a Colab-specific function to display images

###############################################################
# Step 3: Load the YOLOv8s pre-trained model
#         YOLOv8 small model (s stands for small).
#         The model is loaded and ready to detect objects in images.
model = YOLO("yolov8s.pt")
#
# show model characteristics:
# print(model.model)  # gives the underlying PyTorch model
total_params = sum(p.numel() for p in model.model.parameters())
trainable_params = sum(p.numel() for p in model.model.parameters() if p.requires_grad)
print('\n############')
print('YOLO model characteristics:')
print("Total parameter number:", total_params)
print("Trainable parameter number:", trainable_params)
#
# The sub-modules number includes convolutional, batch norm, activation,...
num_layers = len(list(model.model.modules()))
print("Number of layers/modules:", num_layers)
#
#################
from collections import defaultdict
#
# Create a dictionary to store counts per dtype
dtype_counts = defaultdict(int)
#
# Loop through all model parameters
for param in model.model.parameters():
    dtype_counts[param.dtype] += param.numel()  # numel() counts total elements
#
# Print results
for dtype, count in dtype_counts.items():
    print(f"Parameter precision: {dtype}: {count} parameters")
print('############\n')





#################################################
# Step 4: Upload your image file to Colab
#         This opens a file uploader in Colab.
#         You can select an image from your computer.
#         uploaded is a dictionary with the filename as key and file data as value.
from google.colab import files
uploaded = files.upload()

# Assuming you uploaded only one image
image_path = list(uploaded.keys())[0]
print(f'image_path = {image_path}')

# Step 5: Run object detection on the image
#         model.predict() runs the YOLO model on the image.
#         source=image_path tells the model which image to analyze.
#         results is a list of detection outputs, one for each image (here only one).
results = model.predict(source=image_path)

print(f'type of results = {type(results)}')
print(f'len(results) = {len(results)}')

# Step 6: Visualize the results
#         results[0].plot() draws bounding boxes and labels on the detected objects and returns an image array.
output_image = results[0].plot()
print(f'image size = {output_image.shape}')

# Display the result in Colab
cv2_imshow(output_image)

# Step 7: Optionally, save the output image
cv2.imwrite("detected_image.jpg", output_image)
print("Detection saved as detected_image.jpg")



# Crop detected people (it provides cropped regions of people):

from PIL import Image

img = Image.open(image_path)

people_counter = 0
crops = []
for result in results:
    for box in result.boxes:
        cls_id = int(box.cls[0])
        if result.names[cls_id] == "person":
            people_counter = people_counter + 1
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cropped = img.crop((x1, y1, x2, y2))
            crops.append(cropped)
print(f'\n Number of people recognized = {people_counter}')


##############################################
# Pass to an LLM with vision support:

from openai import OpenAI
import base64
from io import BytesIO

client = OpenAI()

def pil_to_base64(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

for i, crop in enumerate(crops):
    img_b64 = pil_to_base64(crop)

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # vision-capable LLM
        messages=[
            {"role": "system", "content": "You are an assistant that classifies emotions in faces."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Does this person look happy or sad?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                ],
            },
        ],
    )

    print(f"Person {i+1}: {response.choices[0].message.content}")
