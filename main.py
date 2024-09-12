import cv2 as cv
import numpy as np
import torch
import os
import torchvision
import socketServer
from ultralytics import YOLO


# Check that the correct versions are installed
print(torch.__version__)
print(torchvision.__version__)
print(torch.version.cuda)

# Yolo classes
names = {0: 'person', 1: 'bicycle', 2: 'car',
         3: 'motorcycle',
         4: 'airplane',
         5: 'bus',
         6: 'train',
         7: 'truck',
         8: 'boat',
         9: 'traffic light',
         10: 'fire hydrant',
         11: 'stop sign',
         12: 'parking meter',
         13: 'bench',
         14: 'bird',
         15: 'cat',
         16: 'dog',
         17: 'horse',
         18: 'sheep',
         19: 'cow',
         20: 'elephant',
         21: 'bear',
         22: 'zebra',
         23: 'giraffe',
         24: 'backpack',
         25: 'umbrella',
         26: 'handbag',
         27: 'tie',
         28: 'suitcase',
         29: 'frisbee',
         30: 'skis',
         31: 'snowboard',
         32: 'sports ball',
         33: 'kite',
         34: 'baseball bat',
         35: 'baseball glove',
         36: 'skateboard',
         37: 'surfboard',
         38: 'tennis racket',
         39: 'bottle',
         40: 'wine glass',
         41: 'cup',
         42: 'fork',
         43: 'knife',
         44: 'spoon',
         45: 'bowl',
         46: 'banana',
         47: 'apple',
         48: 'sandwich',
         49: 'orange',
         50: 'broccoli',
         51: 'carrot',
         52: 'hot dog',
         53: 'pizza',
         54: 'donut',
         55: 'cake',
         56: 'chair',
         57: 'couch',
         58: 'potted plant',
         59: 'bed',
         60: 'dining table',
         61: 'toilet',
         62: 'tv',
         63: 'laptop',
         64: 'mouse',
         65: 'remote',
         66: 'keyboard',
         67: 'cell phone',
         68: 'microwave',
         69: 'oven',
         70: 'toaster',
         71: 'sink',
         72: 'refrigerator',
         73: 'book',
         74: 'clock',
         75: 'vase',
         76: 'scissors',
         77: 'teddy bear',
         78: 'hair drier',
         79: 'toothbrush'}

# Find the absolute path to the video. This fixes a bug
video_path = "testVideo0-hasBackgroundAudio.mp4"
print("Absolute path:", os.path.abspath(video_path))

# Starts the socket server
socketServer.start_server()

cap = cv.VideoCapture(video_path)

# Using the medium sized model
model = YOLO("yolov8m.pt")

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Shows the FPS
'''
fps = cap.get(cv.CAP_PROP_FPS)
print(f"Frames per second: {fps}")
'''

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    results = model(frame)
    results = results[0]
    boundBox = np.array(results.boxes.xyxy.cpu(), dtype="int")
    classes = np.array(results.boxes.cls.cpu(), dtype="int")
    confidences = np.array(results.boxes.conf.cpu(), dtype="float")  # Get confidence scores

    for cls, boundary, confidence in zip(classes, boundBox, confidences):
        (x, y, x2, y2) = boundary
        cv.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)

        label = f"{names[cls]} {confidence:.2f}"  # Display class and confidence
        cv.putText(frame, label, (x, y - 5), cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 225), 2)


    cv.imshow("Img", frame)

    key = cv.waitKey(12)

cap.release()
cv.destroyAllWindows()
