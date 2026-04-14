from rest_framework.decorators import api_view
from rest_framework.response import Response
from .registry import TOOLS


@api_view(["POST"])
def mcp_server(request):
    tool_name = request.data.get("tool")
    args = request.data.get("arguments", {})

    tool = TOOLS.get(tool_name)

    if not tool:
        return Response({"error": "Unknown tool"})

    result = tool(args)
    return Response(result)
