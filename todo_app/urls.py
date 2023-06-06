from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from todo_app.api.views import TaskDetail, ListAddTask, ListAddTodoList, TodoListDetail, FilterTodoList, FilterTask

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("path-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("api/todo-lists/", ListAddTodoList.as_view(), name="all-todo-lists"),
    path("api/todo-lists/filter", FilterTodoList.as_view(), name="filter-todo-lists"),
    path("api/todo-lists/<uuid:pk>", TodoListDetail.as_view(), name="todo-list-detail"),
    path("api/todo-lists/<uuid:pk>/tasks/", ListAddTask.as_view(), name="list-add-tasks"),
    path("api/todo-lists/<uuid:pk>/tasks/filter", FilterTask.as_view(), name="filter-tasks"),
    path("api/todo-lists/<uuid:pk>/tasks/<uuid:task_pk>", TaskDetail.as_view(), name="task-detail"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
