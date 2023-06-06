from rest_framework import serializers
from django.contrib.auth.models import User


from todo_app.models import Item, TodoList


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "done"]
        read_only_fields = ["id", "todo_list"]

    def create(self, validated_data, **kwargs):
        """Validates that an Item can't be duplicated in the same list."""
        validated_data["todo_list_id"] = self.context["request"].parser_context["kwargs"]["pk"]

        if TodoList.objects.get(id=self.context["request"].parser_context["kwargs"]["pk"]).todo_items.filter(
            name=validated_data["name"]
        ):
            raise serializers.ValidationError("There's already this item on the list")

        return super(ItemSerializer, self).create(validated_data)


class TodoListSerializer(serializers.ModelSerializer):
    todo_items = ItemSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    # undone_items = serializers.SerializerMethodField()

    class Meta:
        model = TodoList
        fields = ["id", "name", "todo_items", "owner"]

    # def get_undone_items(self, obj):
    #     return [{"name": item.name} for item in obj.item.filter(done=False)]
