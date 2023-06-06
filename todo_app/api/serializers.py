from rest_framework import serializers

from todo_app.models import Task, TodoList, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "name", "done"]
        read_only_fields = ["id", "todo_list"]

    def create(self, validated_data, **kwargs):
        """Validates that a Task can't be duplicated in the same todo list."""
        todo_list_id = self.context["view"].kwargs["pk"]

        if Task.objects.filter(todo_list_id=todo_list_id, name=validated_data["name"]).exists():
            raise serializers.ValidationError("This task is already on the list!")

        return super(TaskSerializer, self).create(validated_data)


class TodoListSerializer(serializers.ModelSerializer):
    todo_tasks = TaskSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = TodoList
        fields = ["id", "name", "todo_tasks", "owner", "archived"]
