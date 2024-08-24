import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from home import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizza.settings')

# Define your HTTP application (Django's ASGI application)
django_application = get_asgi_application()

# Define your WebSocket routes
ws_patterns = [
    path('ws/pizza/<order_id>/', consumers.OrderProgress.as_asgi()),  # Ensure proper path and consumer
    # Add other WebSocket routes here if needed
]

# Define the ASGI application
application = ProtocolTypeRouter({
    "http": django_application,  # Handles HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(ws_patterns)  # Handles WebSocket connections
    ),
})
