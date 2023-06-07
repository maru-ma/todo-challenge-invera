from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from .api.views.tasks import FilterTask, ListAddTaskView, TaskDetailView
from .api.views.todo_list import FilterTodoList, ListAddTodoListView, TodoListDetailView
from .api.views.user import UserRegistrationView

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("users/", UserRegistrationView.as_view(), name="create-user"),
    path("api/todo-lists/", ListAddTodoListView.as_view(), name="all-todo-lists"),
    path("api/todo-lists/filter", FilterTodoList.as_view(), name="filter-todo-lists"),
    path("api/todo-lists/<uuid:pk>", TodoListDetailView.as_view(), name="todo-list-detail"),
    path("api/todo-lists/<uuid:pk>/tasks/", ListAddTaskView.as_view(), name="list-add-tasks"),
    path("api/todo-lists/<uuid:pk>/tasks/filter", FilterTask.as_view(), name="filter-tasks"),
    path("api/todo-lists/<uuid:pk>/tasks/<uuid:task_pk>", TaskDetailView.as_view(), name="task-detail"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
