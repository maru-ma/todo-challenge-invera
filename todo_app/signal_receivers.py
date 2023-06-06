from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Item, TodoList


@receiver(post_save, sender=Item)
def interaction_with_todo_list(sender, instance, **kwargs):
    TodoList.objects.get(id=instance.todo_list.id).save(update_fields=["updated"])
