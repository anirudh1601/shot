"""
ASGI config for audiochat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
import webrtc.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audiochat.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket':AuthMiddlewareStack(
    	URLRouter(
    		webrtc.routing.websocket_urlpatterns,

    	)

    )
    # Just HTTP for now. (We can add other protocols later.)
})

