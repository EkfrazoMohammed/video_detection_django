# myapp/routing.py
from django.urls import path
from .consumers import VideoProcessingConsumer

websocket_urlpatterns = [
    path('ws/video/', VideoProcessingConsumer.as_asgi()),  # Match your WebSocket URL
]
