from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Task, TodoList


@receiver(post_save, sender=Task)
def interaction_with_todo_list(sender, instance, **kwargs):
    """
    Signal receiver for interacting with the associated todo list after a task is saved.

    When a task is saved, this receiver updates the `updated` field of the associated todo list.
    """
    TodoList.objects.get(id=instance.todo_list.id).save(update_fields=["updated"])
