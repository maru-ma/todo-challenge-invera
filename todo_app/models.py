import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class TodoList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="todo_tasks")
    created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    pass
