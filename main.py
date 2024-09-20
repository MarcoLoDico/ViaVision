import cv2 as cv
import numpy as np
import torch
import time
import socketServer
from sharedData import SharedData
import coordinateCalculator
from ultralytics import YOLO
import mss
import multiprocessing
from multiprocessing.managers import BaseManager


class SharedDataManager(BaseManager):
    pass


SharedDataManager.register('SharedData', SharedData)


def main_loop(shared_data_obj):
    global prev_time
    prev_time = 0

    # Important YOLO class labels
    names = {2: 'car', 11: 'stop sign'}

    # Load YOLO model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = YOLO("yolov8s.pt").to(device)

    # Target frame rate (FPS)
    target_fps = 30
    frame_interval = 1 / target_fps

    # Screen capture setup using mss
    sct = mss.mss()
    monitor = {"top": 0, "left": 0, "width": 2560, "height": 1440}

    prev_time = 0

    while True:
        current_time = time.time()
        if (current_time - prev_time) >= frame_interval:
            prev_time = current_time  # Update the timer

            # Capture the screen
            sct_img = sct.grab(monitor)
            frame = np.array(sct_img)
            frame = cv.cvtColor(frame, cv.COLOR_BGRA2BGR)

            # Access the current coordinates from shared data
            current_coordinates = shared_data_obj.get_data()  # Use get_data from SharedData class
            print(f"Shared data: {current_coordinates}")

            if current_coordinates is None:
                current_coordinates = "0,0,0,0"

            # YOLO detection
            with torch.no_grad():  # Reduces memory consumption
                results = model(frame, conf=0.2, classes=[11])  # Focus on stop signs

            results = results[0]
            boundBox = np.array(results.boxes.xyxy.cpu(), dtype="int")
            classes = np.array(results.boxes.cls.cpu(), dtype="int")
            confidences = np.array(results.boxes.conf.cpu(), dtype="float")

            for cls, boundary, confidence in zip(classes, boundBox, confidences):
                (x, y, x2, y2) = boundary

                # Calculate size and location on screen
                width = x2 - x
                height = y2 - y
                center_x = x + width // 2
                center_y = y + height // 2

                # Print details of the detected object
                print(f"Detected {names[cls]}:")
                print(f" - Location (top-left): ({x}, {y})")
                print(f" - Size (width x height): {width} x {height}")
                print(f" - Center location: ({center_x}, {center_y})")

                # Draw bounding boxes on the original frame
                cv.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)
                label = f"{names[cls]} {confidence:.2f}"
                cv.putText(frame, label, (x, y - 5), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 225), 2)

                predicted_coordinates = coordinateCalculator.predict_coordinates(height, center_x, current_coordinates)
                print(f"Predicted coordinates: {predicted_coordinates}")

            # Display FPS on the frame
            fps_text = f"FPS: {int(1 / frame_interval)}"
            cv.putText(frame, fps_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display the processed frame
            cv.imshow("Screen Capture", cv.resize(frame, (3070, 1920)))

        # Press 'q' to exit the loop
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()


if __name__ == "__main__":
    manager = SharedDataManager()
    manager.start()

    shared_data = manager.SharedData()

    socket_process = multiprocessing.Process(
        target=socketServer.run_socket_server, args=(shared_data,)
    )
    socket_process.start()

    main_loop(shared_data)

    socket_process.join()
