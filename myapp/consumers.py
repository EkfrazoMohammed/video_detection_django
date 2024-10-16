import json
import cv2
import base64
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from ultralytics import YOLO  # Ensure you have the ultralytics package installed


class VideoProcessingConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = YOLO(
            "yolov5n.pt"
        )  # Load a lighter YOLO model for faster processing
        self.is_connected = False  # Flag to check if the consumer is connected

    async def connect(self):
        await self.accept()
        self.is_connected = True  # Set connected flag
        print("WebSocket connected")

    async def disconnect(self, close_code):
        self.is_connected = False  # Clear connected flag
        print("WebSocket disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Check for video URL
        if "video_url" in data:
            video_url = data["video_url"]
            await self.process_video(video_url)
        elif "message" in data and data["message"].strip().lower() == "hi":
            await self.send_hello_response()

    async def process_video(self, video_url):
        cap = cv2.VideoCapture(video_url)
        if not cap.isOpened():
            print("Error: Unable to open video source.")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break  # Exit if no more frames are available

                # Resize frame for faster processing
                frame = cv2.resize(
                    frame, (320, 240)
                )  # Reduced resolution for faster processing

                # Check if the consumer is still connected before processing the frame
                if not self.is_connected:
                    print("Processing stopped: WebSocket is disconnected.")
                    break

                # Process the frame asynchronously with YOLO
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, self.model, frame)

                # Draw bounding boxes and labels on the frame
                annotated_frame = result[0].plot()

                # Convert the annotated frame to JPG and encode to base64
                _, buffer = cv2.imencode(".jpg", annotated_frame)
                jpg_as_text = base64.b64encode(buffer).decode("utf-8")

                # Send the annotated frame back to the client every 3rd frame
                if frame_count % 3 == 0:  # Skip frames to reduce the load
                    await self.send(
                        text_data=json.dumps(
                            {
                                "frame": jpg_as_text,
                                "frame_number": frame_count,
                            }
                        )
                    )

                frame_count += 1

                # Introduce a slight delay to avoid overwhelming the server
                await asyncio.sleep(0.01)  # Short sleep to allow for other tasks

        except Exception as e:
            print("Error during frame processing:", str(e))

        finally:
            cap.release()  # Release the video capture object

        # Notify the client that processing is complete if still connected
        if self.is_connected:
            await self.send(
                text_data=json.dumps(
                    {
                        "processing_complete": True,
                        "message": "Video processing completed.",
                    }
                )
            )

    async def send_hello_response(self):
        # Send a simple hello response
        await self.send(text_data=json.dumps({"message": "hello"}))
