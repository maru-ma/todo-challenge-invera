from rest_framework import generics

from .serializers import TodoItemSerializer, TodoListSerializer
from todo_app.models import TodoItem, TodoList

class ListAddTodoList(generics.ListCreateAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer


class TodoListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer


class ListAddTodoItem(generics.ListCreateAPIView):
    serializer_class = TodoItemSerializer

    def get_queryset(self):
        todo_list_pk = self.kwargs["pk"]
        queryset = TodoItem.objects.filter(todo_list=todo_list_pk).order_by("done")
        return queryset

class TodoItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoItem.objects.all()
    serialaizer_class = TodoItemSerializer
    lookup_url_kwarg = "item_pk"
