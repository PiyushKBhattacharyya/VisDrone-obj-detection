from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import torch
import os
import time
from ultralytics import YOLO
import numpy as np
from utils import detect_power_level, euclidean_distance

app = FastAPI()

# Allow CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Dataset folder if not present
os.makedirs('Dataset', exist_ok=True)

# Detect system power level
power_mode, device = detect_power_level()
print(f"Power Mode: {power_mode}, Device: {device}")

# Select appropriate model based on power mode
model_map = {
    "HIGH": ("yolov8m.pt", 1, 0.25, 60),
    "MEDIUM": ("yolov8s.pt", 2, 0.3, 45),
    "LOW": ("yolov8n.pt", 3, 0.35, 20)
}
model_path, frame_skip, conf_threshold, fps_limit = model_map[power_mode]

# Load YOLO model
model = YOLO(model_path)
model.to(device)

# Tracking variables
persons_tracker = []
face_id_counter = 0

def generate_frames():
    """Function to capture frames from live feed and perform person detection."""
    global persons_tracker, face_id_counter

    # Open webcam (use RTSP URL if needed)
    video_source = 0  # Change this to an RTSP URL if using a drone
    cap = cv2.VideoCapture(video_source)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame, exiting...")
            break

        # Flip the frame for mirroring effect
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 480))

        # Run YOLO detection with streaming
        results = model(frame, verbose=False, stream=True, conf=conf_threshold)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())

                # Ensure detection is for "person" only
                if model.names[cls] == "person" and conf >= conf_threshold:
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    new_center = (center_x, center_y)

                    # Check if this person is already tracked
                    is_new_person = True
                    for existing_person in persons_tracker:
                        if euclidean_distance(new_center, existing_person) < 100:
                            is_new_person = False
                            break

                    if is_new_person:
                        # If it's a new person, save the image and update tracker
                        cropped_image = frame[y1:y2, x1:x2]
                        timestamp = time.strftime("%Y%m%d-%H%M%S")
                        file_name = f"Dataset/person_{timestamp}_{face_id_counter}.jpg"
                        cv2.imwrite(file_name, cropped_image)

                        persons_tracker.append(new_center)
                        face_id_counter += 1
                        print(f"Saved detected person image to: {file_name}")

                    # Draw bounding box
                    label = f"Person {conf:.2f}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the number of unique persons detected
        cv2.putText(frame, f"Unique People: {len(persons_tracker)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Encode the frame for streaming
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.get("/")
async def root():
    return {"message": "Live Drone Detection API Running!"}

@app.get("/video-feed/")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/unique-persons/")
async def get_unique_person_count():
    return {"unique_persons_detected": len(persons_tracker)}
