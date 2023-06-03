from django.urls import include, path
from todo_app.api.views import (ListAddTodoItem, ListAddTodoList,
                                TodoItemDetail, TodoListDetail)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView 

urlpatterns = [
    path("api/todo-lists/", ListAddTodoList.as_view(), name="all-todo-lists"),
    path("api/todo-lists/<uuid:pk>", TodoListDetail.as_view(), name="todo-list-detail"),
    path("api/todo-lists/<uuid:pk>/todo-items", ListAddTodoItem.as_view(), name="all-todo-items"),
    path("api/todo-lists/<uuid:pk>/todo-items/<uuid:item_pk>", TodoItemDetail.as_view(), name="todo-item-detail"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]