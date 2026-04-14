from django.urls import path
from store.views import mcp_server

urlpatterns = [
    path("mcp/", mcp_server),
]
