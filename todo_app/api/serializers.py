from rest_framework import serializers


from todo_app.models import TodoItem, TodoList



class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ["id", "name", "done"]
        read_only_fields = ["id", ]

    def create(self, validated_data, **kwargs):
        validated_data["todo_list_id"] =  self.context["request"].parser_context["kwargs"]["pk"]

        if TodoList.objects.get(id=self.context["request"].parser_context["kwargs"]["pk"]
                                    ).todo_items.filter(name=validated_data["name"]):
            raise serializers.ValidationError("There's already this item on the list")
    
        return super(TodoItemSerializer, self).create(validated_data)

class TodoListSerializer(serializers.ModelSerializer):
    todo_items = TodoItemSerializer(many=True, read_only=True)

    class Meta:
        model = TodoList
        fields = ["id", "name", "todo_items"]