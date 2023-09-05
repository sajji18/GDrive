"""
ASGI config for GDrive project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import iitr_drive.routing 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GDrive.settings')

application = get_asgi_application()

 # Import your app's routing configuration
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            iitr_drive.routing.websocket_urlpatterns  # Use your app's WebSocket routing
        )
    ),
})
