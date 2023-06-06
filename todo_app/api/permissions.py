from rest_framework import permissions

from todo_app.models import TodoList


class TodoListOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or (request.user == obj.owner):
            return True

        return False


class ItemTodoListOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or (request.user == obj.todo_list.owner):
            return True

        return False


# REVISAR
class AllItemsTodoListOwnerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        current_todo_list = TodoList.objects.get(pk=view.kwargs.get("pk"))
        if request.user == current_todo_list.owner:
            return True

        return False
