from django.urls import path
from .import consumers

websocket_urlpatterns = [
	path('',consumers.AudioConsumer.as_asgi(),name='audio')
	
]