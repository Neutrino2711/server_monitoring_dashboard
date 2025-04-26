from django.urls import re_path 
from . import consumers 

websocket_urlpatterns = [
    re_path(r'ws/server-metric/$', consumers.ServerMetricsConsumer.as_asgi()),
]