from datetime import datetime, timedelta
from unittest import mock

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from todo_app.models import Item, TodoList


@pytest.mark.django_db
def test_create_todo_list(create_user, create_authenticated_client):
    url = reverse("all-todo-lists")
    data = {
        "name": "Super",
    }
    client = create_authenticated_client(create_user())
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert TodoList.objects.get().name == "Super"


@pytest.mark.django_db
def test_list_all_todo_lists(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Super", user)
    another_todo_list = create_todo_list("Books", user)

    url = reverse("all-todo-lists")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Books"
    assert response.data[1]["name"] == "Super"


@pytest.mark.django_db
def test_retrieve_todo_list_by_id(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Super", user)

    url = reverse("todo-list-detail", args=[todo_list.id])

    response = client.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Super"


@pytest.mark.django_db
def test_todo_list_includes_only_corresponding_items(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    client = create_authenticated_client(user)

    todo_list = create_todo_list("Super", user)
    another_todo_list = create_todo_list("Books", user)

    Item.objects.create(todo_list=todo_list, name="Eggs", done=False)
    Item.objects.create(todo_list=another_todo_list, name="The seven sisters", done=False)

    url = reverse("todo-list-detail", args=[todo_list.id])
    response = client.get(url)

    assert len(response.data["todo_items"]) == 1
    assert response.data["todo_items"][0]["name"] == "Eggs"


@pytest.mark.django_db
def test_update_todo_list_name(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    client = create_authenticated_client(user)

    todo_list = create_todo_list("Super", user=user)

    url = reverse("todo-list-detail", args=[todo_list.id])

    data = {
        "name": "Fruits",
    }

    response = client.put(url, data=data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Fruits"


@pytest.mark.django_db
def test_delete_todo_list(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    client = create_authenticated_client(user)

    todo_list = create_todo_list("Super", user=user)

    url = reverse("todo-list-detail", args=[todo_list.id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert len(TodoList.objects.all()) == 0


@pytest.mark.django_db
def test_update_todo_list_restricted_to_owner(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    todo_list_owner = User.objects.create_user("owner", "owner@todoapp.com", "something")
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Super", todo_list_owner)

    url = reverse("todo-list-detail", args=[todo_list.id])

    data = {
        "name": "Food",
    }

    response = client.put(url, data=data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_partial_update_todo_list_restricted_to_owner(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    todo_list_owner = User.objects.create_user("owner", "owner@todoapp.com", "something")
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Super", todo_list_owner)

    url = reverse("todo-list-detail", args=[todo_list.id])

    data = {
        "name": "Food",
    }

    response = client.patch(url, data=data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_todo_list_restricted_to_owner(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    todo_list_creator = User.objects.create_user("Owner", "owner@todoapp.com", "something")
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Super", todo_list_creator)

    url = reverse("todo-list-detail", args=[todo_list.id])

    response = client.delete(url, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_client_retrieves_only_todo_list_of_owner(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    todo_list = create_todo_list("Super", user)

    another_user = User.objects.create_user("SomeoneElse", "someone@else.com", "something")
    create_todo_list("Books", another_user)

    client = create_authenticated_client(user)
    url = reverse("all-todo-lists")
    response = client.get(url)

    assert len(response.data) == 1
    assert response.data[0]["name"] == "Super"


@pytest.mark.django_db
def test_admin_can_retrieve_todo_list(create_user, create_todo_list, admin_client):

    user = create_user()
    todo_list = create_todo_list("Super", user)

    url = reverse("todo-list-detail", args=[todo_list.id])

    response = admin_client.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_correct_order_todo_lists(create_user, create_authenticated_client):
    url = reverse("all-todo-lists")
    user = create_user()
    client = create_authenticated_client(user)

    old_time = datetime.now() - timedelta(days=1)
    older_time = datetime.now() - timedelta(days=100)

    with mock.patch("django.utils.timezone.now") as mock_now:
        mock_now.return_value = old_time
        TodoList.objects.create(name="Old", owner=user)

        mock_now.return_value = older_time
        TodoList.objects.create(name="Oldest", owner=user)

    TodoList.objects.create(name="New", owner=user)

    response = client.get(url)

    assert response.data[0]["name"] == "New"
    assert response.data[1]["name"] == "Old"
    assert response.data[2]["name"] == "Oldest"


@pytest.mark.django_db
def test_todo_lists_order_changed_when_item_marked_purchased(create_user, create_authenticated_client):

    user = create_user()
    client = create_authenticated_client(user)

    more_recent_time = datetime.now() - timedelta(days=1)
    older_time = datetime.now() - timedelta(days=20)

    with mock.patch("django.utils.timezone.now") as mock_now:
        mock_now.return_value = older_time
        older_list = TodoList.objects.create(name="Older", owner=user)
        item_on_older_list = Item.objects.create(name="Milk", done=False, todo_list=older_list)

        mock_now.return_value = more_recent_time
        TodoList.objects.create(name="Recent", updated=datetime.now() - timedelta(days=100), owner=user)

    todo_item_url = reverse("item-detail", kwargs={"pk": older_list.id, "item_pk": item_on_older_list.id})
    todo_lists_url = reverse("all-todo-lists")

    data = {"done": True}

    client.patch(todo_item_url, data)

    response = client.get(todo_lists_url)

    assert response.data[1]["name"] == "Recent"
    assert response.data[0]["name"] == "Older"
