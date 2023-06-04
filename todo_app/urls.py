from django.urls import include, path
from todo_app.api.views import ListAddItem, ListAddTodoList, ItemDetail, TodoListDetail
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/todo-lists/", ListAddTodoList.as_view(), name="all-todo-lists"),
    path("api/todo-lists/<uuid:pk>", TodoListDetail.as_view(), name="todo-list-detail"),
    path("api/todo-lists/<uuid:pk>/tems", ListAddItem.as_view(), name="all-items"),
    path("api/todo-lists/<uuid:pk>/items/<uuid:item_pk>", ItemDetail.as_view(), name="item-detail"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
