# myapp/video_processing.py

import json
import base64
import cv2
import asyncio
from ultralytics import YOLO

class VideoObjectDetection:
    def __init__(self, video_url, model_path="yolov5s.pt"):
        self.video_url = video_url
        self.model = YOLO(model_path)  # Load YOLO model

    async def process_video(self, send_frame):
        cap = cv2.VideoCapture(self.video_url)
        if not cap.isOpened():
            print("Error: Unable to open video source.")
            return

        try:
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    break

                # Process the frame asynchronously
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, self.model, frame)

                # Draw bounding boxes and labels on the frame
                annotated_frame = result[0].plot()

                # Encode the frame as a JPEG image
                ret, buffer = cv2.imencode('.jpg', annotated_frame)
                if not ret:
                    continue

                # Convert the image to base64
                frame_image = base64.b64encode(buffer).decode('utf-8')

                # Send the frame through the WebSocket
                await send_frame(frame_image)

                await asyncio.sleep(0.01)  # Yield control back to the event loop

        except Exception as e:
            print("Error during video processing:", str(e))
        
        finally:
            cap.release()
