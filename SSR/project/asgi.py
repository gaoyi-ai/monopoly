"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from monopoly.consumers.join import QueryAuthMiddleware

django_asgi_app = get_asgi_application()

import monopoly.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        QueryAuthMiddleware(
            URLRouter(
                monopoly.routing.websocket_urlpatterns
            )
        )
    ),
})
