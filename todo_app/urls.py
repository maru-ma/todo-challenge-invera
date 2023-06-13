from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

from .api.views.tasks import FilterTask, TaskViewSet
from .api.views.todo_list import FilterTodoList, TodoListViewSet
from .api.views.user import UserRegistrationView


task_router = routers.SimpleRouter()
task_router.register(r"tasks", TaskViewSet, basename="tasks")
todo_list_router = routers.SimpleRouter()
todo_list_router.register(r"todo-lists", TodoListViewSet, basename="todo-lists")

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("users/", UserRegistrationView.as_view(), name="create-user"),
    path("api/todo-lists/filter", FilterTodoList.as_view(), name="filter-todo-lists"),
    path("api/todo-lists/<uuid:todo_list_pk>/tasks/filter", FilterTask.as_view(), name="filter-tasks"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/todo-lists/<uuid:todo_list_pk>/", include(task_router.urls)),
    path("api/", include(todo_list_router.urls)),
]
