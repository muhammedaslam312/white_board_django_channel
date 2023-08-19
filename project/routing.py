from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from whiteboard.consumer import BoardConsumer


application = ProtocolTypeRouter(
    {
        "websocket": AllowedHostsOriginValidator(
            URLRouter(
                [
                    # Define your WebSocket consumers here
                    # Example:
                    path("white_board/", BoardConsumer),
                ]
            )
        )
        # ...
    }
)
