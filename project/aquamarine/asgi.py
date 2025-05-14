"""
ASGI config for aquamarine project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

import carwash.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aquamarine.settings')

asgi_application = get_asgi_application()  # new

application = ProtocolTypeRouter({
    "http": asgi_application,
    "websocket":
        AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(carwash.routing.websocket_urlpatterns)
            ),
        )
})
