# # # import json
# # # import cv2
# # # import base64
# # # import asyncio
# # # from channels.generic.websocket import AsyncWebsocketConsumer
# # # from ultralytics import YOLO  # Ensure you have the ultralytics package installed

# # # class VideoProcessingConsumer(AsyncWebsocketConsumer):
# # #     def __init__(self, *args, **kwargs):
# # #         super().__init__(*args, **kwargs)
# # #         self.model = YOLO("yolov5s.pt")  # Load the YOLO model

# # #     async def connect(self):
# # #         await self.accept()
# # #         print("WebSocket connected")

# # #     async def disconnect(self, close_code):
# # #         print("WebSocket disconnected")

# # #     async def receive(self, text_data):
# # #         data = json.loads(text_data)

# # #         # Extract the video URL from the received data
# # #         video_url = data.get('video_url')
# # #         if video_url:
# # #             await self.process_video(video_url)

# # #     async def process_video(self, video_url):
# # #         # Open the video file
# # #         cap = cv2.VideoCapture(video_url)
# # #         if not cap.isOpened():
# # #             print("Error: Unable to open video source.")
# # #             return

# # #         frame_count = 0
# # #         fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frame rate of the video
# # #         delay = 1 / fps  # Calculate delay based on FPS
# # #         total_duration = 15  # Process frames for 15 seconds
# # #         max_frames = int(total_duration * fps)  # Calculate maximum number of frames to process

# # #         try:
# # #             while cap.isOpened() and frame_count < max_frames:
# # #                 ret, frame = cap.read()
# # #                 if not ret:
# # #                     break  # Exit if no more frames are available

# # #                 # Process the frame asynchronously with YOLO
# # #                 loop = asyncio.get_event_loop()
# # #                 result = await loop.run_in_executor(None, self.model, frame)

# # #                 # Draw bounding boxes and labels on the frame
# # #                 annotated_frame = result[0].plot()

# # #                 # Convert the annotated frame to JPG and encode to base64
# # #                 _, buffer = cv2.imencode('.jpg', annotated_frame)
# # #                 jpg_as_text = base64.b64encode(buffer).decode('utf-8')

# # #                 # Send the annotated frame back to the client
# # #                 await self.send(text_data=json.dumps({
# # #                     'frame': jpg_as_text,
# # #                     'frame_number': frame_count,
# # #                 }))
# # #                 frame_count += 1

# # #                 # Wait based on the video's frame rate to keep it in sync
# # #                 await asyncio.sleep(delay)

# # #         except Exception as e:
# # #             print("Error during frame processing:", str(e))

# # #         finally:
# # #             cap.release()  # Release the video capture object

# # #         # Notify the client that processing is complete
# # #         await self.send(text_data=json.dumps({
# # #             'processing_complete': True,
# # #             'message': 'Video processing completed.'
# # #         }))

# import json
# import cv2
# import base64
# import asyncio
# from channels.generic.websocket import AsyncWebsocketConsumer
# from ultralytics import YOLO  # Ensure you have the ultralytics package installed

# class VideoProcessingConsumer(AsyncWebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.model = YOLO("yolov5s.pt")  # Load the YOLO model

#     async def connect(self):
#         await self.accept()
#         print("WebSocket connected")

#     async def disconnect(self, close_code):
#         print("WebSocket disconnected")

#     async def receive(self, text_data):
#         data = json.loads(text_data)

#         # Check for video URL or a simple greeting message
#         if 'video_url' in data:
#             video_url = data['video_url']
#             await self.process_video(video_url)
#         elif 'message' in data and data['message'].strip().lower() == 'hi':
#             await self.send_hello_response()

#     async def process_video(self, video_url):
#         # Open the video file
#         cap = cv2.VideoCapture(video_url)
#         if not cap.isOpened():
#             print("Error: Unable to open video source.")
#             return

#         frame_count = 0
#         fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frame rate of the video
#         delay = 1 / fps  # Calculate delay based on FPS
#         total_duration = 15  # Process frames for 15 seconds
#         max_frames = int(total_duration * fps)  # Calculate maximum number of frames to process

#         try:
#             while cap.isOpened() and frame_count < max_frames:
#                 ret, frame = cap.read()
#                 if not ret:
#                     break  # Exit if no more frames are available

#                 # Process the frame asynchronously with YOLO
#                 loop = asyncio.get_event_loop()
#                 result = await loop.run_in_executor(None, self.model, frame)

#                 # Draw bounding boxes and labels on the frame
#                 annotated_frame = result[0].plot()

#                 # Convert the annotated frame to JPG and encode to base64
#                 _, buffer = cv2.imencode('.jpg', annotated_frame)
#                 jpg_as_text = base64.b64encode(buffer).decode('utf-8')

#                 # Send the annotated frame back to the client
#                 await self.send(text_data=json.dumps({
#                     'frame': jpg_as_text,
#                     'frame_number': frame_count,
#                 }))
#                 frame_count += 1

#                 # Wait based on the video's frame rate to keep it in sync
#                 await asyncio.sleep(delay)

#         except Exception as e:
#             print("Error during frame processing:", str(e))

#         finally:
#             cap.release()  # Release the video capture object

#         # Notify the client that processing is complete
#         await self.send(text_data=json.dumps({
#             'processing_complete': True,
#             'message': 'Video processing completed.'
#         }))

#     async def send_hello_response(self):
#         # Send a simple hello response
#         await self.send(text_data=json.dumps({
#             'message': 'hello'
#         }))


import json
import cv2
import base64
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from ultralytics import YOLO  # Ensure you have the ultralytics package installed

class VideoProcessingConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = YOLO("yolov5n.pt")  # Load a lighter YOLO model for faster processing

    async def connect(self):
        await self.accept()
        print("WebSocket connected")

    async def disconnect(self, close_code):
        print("WebSocket disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Check for video URL
        if 'video_url' in data:
            video_url = data['video_url']
            await self.process_video(video_url)
        elif 'message' in data and data['message'].strip().lower() == 'hi':
            await self.send_hello_response()

    async def process_video(self, video_url):
        cap = cv2.VideoCapture(video_url)
        if not cap.isOpened():
            print("Error: Unable to open video source.")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frame rate of the video
        frame_interval = int(fps)  # Process one frame every second
        frame_count = 0

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break  # Exit if no more frames are available

                # Resize frame for faster processing (optional)
                frame = cv2.resize(frame, (640, 480))  # Resize to 640x480 for quicker processing

                # Process the frame asynchronously with YOLO
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, self.model, frame)

                # Draw bounding boxes and labels on the frame
                annotated_frame = result[0].plot()

                # Convert the annotated frame to JPG and encode to base64
                _, buffer = cv2.imencode('.jpg', annotated_frame)
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')

                # Send the annotated frame back to the client every second
                if frame_count % frame_interval == 0:
                    await self.send(text_data=json.dumps({
                        'frame': jpg_as_text,
                        'frame_number': frame_count,
                    }))

                frame_count += 1

                # Skip the appropriate number of frames to send one per second
                await asyncio.sleep(1 / fps)

        except Exception as e:
            print("Error during frame processing:", str(e))

        finally:
            cap.release()  # Release the video capture object

        # Notify the client that processing is complete
        await self.send(text_data=json.dumps({
            'processing_complete': True,
            'message': 'Video processing completed.'
        }))

    async def send_hello_response(self):
        # Send a simple hello response
        await self.send(text_data=json.dumps({
            'message': 'hello'
        }))
