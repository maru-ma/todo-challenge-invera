from rest_framework import generics

from .serializers import ItemSerializer, TodoListSerializer
from todo_app.models import Item, TodoList


class ListAddTodoList(generics.ListCreateAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer


class TodoListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer


class ListAddItem(generics.ListCreateAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        todo_list_pk = self.kwargs["pk"]
        queryset = Item.objects.filter(todo_list=todo_list_pk).order_by("done")
        return queryset


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serialaizer_class = ItemSerializer
    lookup_url_kwarg = "item_pk"
