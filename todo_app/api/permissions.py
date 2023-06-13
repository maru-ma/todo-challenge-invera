from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from todo_app.models import TodoList


class TodoListOwnerOnly(permissions.BasePermission):
    """
    Permission class for TodoList views.

    This permission allows access only to the owner of the TodoList object or superusers.

    Example usage:
    - Superusers have full access to all TodoList objects.
    - Non-superuser owners have access to their own TodoList objects.

    """

    def has_object_permission(self, request, view, obj):
        print(obj.owner)
        if request.user.is_superuser or (request.user == obj.owner):
            return True

        raise PermissionDenied("You do not have permission to access this TodoList.")


class TaskTodoListOwnerOnly(permissions.BasePermission):
    """
    Permission class for Task views.

    This permission allows access only to the owner of the associated TodoList object or superusers.

    Example usage:
    - Superusers have full access to all Task objects.
    - Non-superuser owners have access to Task objects associated with their own TodoList objects.

    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or (request.user == obj.todo_list.owner):
            return True

        raise PermissionDenied({"detail": "You do not have permission to access this TodoList."})


class AllTasksTodoListOwnerOnly(permissions.BasePermission):
    """
    Permission class for ListAddTask view.

    This permission allows access to the view only if the user is a superuser or the owner of the associated TodoList object.

    Example usage:
    - Superusers have full access to the view.
    - Non-superuser owners have access if they own the associated TodoList object.

    """

    def has_permission(self, request, view):
        if (
            request.user.is_superuser
            or TodoList.objects.filter(pk=view.kwargs.get("todo_list_pk"), owner=request.user).exists()
        ):
            return True

        raise PermissionDenied("You do not have permission to access this view.")
