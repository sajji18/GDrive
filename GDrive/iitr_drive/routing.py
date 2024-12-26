# from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from consumers import FileShareConsumer

# application = ProtocolTypeRouter({
#     "websocket": URLRouter([
#         re_path(r'ws/file_share/$', FileShareConsumer.as_asgi()),
#     ]),
# })
