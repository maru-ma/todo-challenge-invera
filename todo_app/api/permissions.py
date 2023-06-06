from rest_framework import permissions

from todo_app.models import TodoList


class TodoListOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or (request.user == obj.owner):
            return True

        return False


class TaskTodoListOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or (request.user == obj.todo_list.owner):
            return True

        return False


# REVISAR
class AllTasksTodoListOwnerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        todo_list_id = view.kwargs.get("pk")
        return TodoList.objects.filter(pk=todo_list_id, owner=request.user).exists()
