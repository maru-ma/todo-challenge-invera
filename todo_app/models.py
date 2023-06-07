import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class TodoList(models.Model):
    """
    Represents a todo list owned by a user.

    Fields:
    - id (UUIDField): The unique identifier for the todo list.
    - name (CharField): The name of the todo list.
    - owner (ForeignKey): The owner of the todo list.
    - archived (BooleanField): Indicates if the todo list is archived.
    - updated (DateTimeField): The last updated timestamp of the todo list.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    """
    Represents a task within a todo list.

    Fields:
    - id (UUIDField): The unique identifier for the task.
    - todo_list (ForeignKey): The todo list that the task belongs to.
    - name (CharField): The name of the task.
    - done (BooleanField): Indicates if the task is completed.
    - created (DateTimeField): The creation timestamp of the task.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="todo_tasks")
    created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    """
    Represents a user account in the system.

    This model is used for authentication and authorization purposes.
    It inherits from Django's built-in AbstractUser model.
    """

    pass
