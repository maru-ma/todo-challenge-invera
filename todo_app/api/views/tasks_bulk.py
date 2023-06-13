# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from drf_spectacular.utils import extend_schema

# @extend_schema(
#     description="Update multiple tasks at once.",
#     request={
#         "description": "List of task IDs and fields to update.",
#         "type": "array",
#         "items": {
#             "type": "object",
#             "properties": {
#                 "id": {"type": "integer", "description": "Task ID."},
#                 "done": {"type": "boolean", "description": "Updated done status."},
#                 # Add more fields as needed
#             },
#         },
#     },
#     responses={
#         status.HTTP_200_OK: {"description": "Tasks updated successfully."},
#         status.HTTP_400_BAD_REQUEST: {"description": "Invalid request payload."},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error."},
#     },
# )
# class BulkUpdateTasksView(APIView):
#     def put(self, request, format=None):
#         tasks = request.data
#         # Perform bulk update logic
#         # ..."""  """

#         return Response(status=status.HTTP_200_OK)
