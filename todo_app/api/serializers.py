from rest_framework import serializers

from todo_app.models import Task, TodoList, User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.

    This serializer is used for serializing and deserializing User objects.
    It handles fields such as username and password.

    Fields:
        - username: The username of the user.
        - password: The password of the user.

    Extra Keyword Arguments:
        - password (write_only): Indicates that the password field is write-only and should not be included
                                 in the serialized representation of the user.
    """

    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for TodoList model.

    This serializer serializes/deserializes TodoList objects and provides
    validation for the data.

    It includes the following fields:
    - id: The unique identifier of the todo list (read-only).
    - name: The name of the todo list.
    - todo_tasks: A list of associated tasks (read-only).
    - owner: The owner of the todo list (read-only).
    - archived: Indicates whether the todo list is archived or not.
    """

    class Meta:
        model = Task
        fields = ["id", "name", "done", "created"]
        read_only_fields = [
            "id",
        ]

    def create(self, validated_data, **kwargs):
        """Validates that a Task can't be duplicated in the same todo list."""
        todo_list_id = self.context["view"].kwargs["pk"]

        if Task.objects.filter(todo_list_id=todo_list_id, name=validated_data["name"]).exists():
            raise serializers.ValidationError("This task is already on the list!")

        validated_data["todo_list_id"] = todo_list_id
        return super(TaskSerializer, self).create(validated_data)


class TodoListSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.

    This serializer serializes/deserializes Task objects and provides
    validation for the data.

    It includes the following fields:
    - id: The unique identifier of the task (read-only).
    - name: The name of the task.
    - description: The description of the task.
    - done: Indicates whether the task is marked as done or not.
    - created: The date and time of task creation (read-only).
    - todo_list: The associated todo list (read-only).
    """

    todo_tasks = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    owner = UserSerializer(read_only=True)

    class Meta:
        model = TodoList
        fields = ["id", "name", "todo_tasks", "owner", "archived"]
