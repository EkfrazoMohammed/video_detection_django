# myapp/urls.py
from django.urls import path
from .views import VideoProcessingView
from .consumers import VideoProcessingConsumer  # Optional for WebSocket

urlpatterns = [
    path('video-url/', VideoProcessingView.as_view(), name='video-url'),
    path('ws/video/', VideoProcessingConsumer.as_asgi(), name='video-websocket'),  # Optional
]
