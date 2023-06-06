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
        validated_data["todo_list_id"] = self.context["request"].parser_context["kwargs"]["pk"]

        if TodoList.objects.get(id=self.context["request"].parser_context["kwargs"]["pk"]).todo_tasks.filter(
            name=validated_data["name"]
        ):
            raise serializers.ValidationError("This task is already on the list!")

        return super(TaskSerializer, self).create(validated_data)


class TodoListSerializer(serializers.ModelSerializer):
    todo_tasks = TaskSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = TodoList
        fields = ["id", "name", "todo_tasks", "owner", "archived"]
