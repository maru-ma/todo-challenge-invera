from datetime import datetime, timedelta
from unittest import mock

import pytest
from django.urls import reverse
from rest_framework import status

from todo_app.models import Task, TodoList, User


@pytest.mark.django_db
def test_create_todo_list(create_user, create_authenticated_client):
    url = "/api/todo-lists/"
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

    url = "/api/todo-lists/"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 2
    assert response.data["results"][0]["name"] == "Books"
    assert response.data["results"][1]["name"] == "Super"


@pytest.mark.django_db
def test_retrieve_todo_list_by_id(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Super", user)

    url = f"/api/todo-lists/{todo_list.id}/"

    response = client.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Super"


@pytest.mark.django_db
def test_todo_list_includes_only_corresponding_tasks(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    client = create_authenticated_client(user)

    todo_list = create_todo_list("Super", user)
    another_todo_list = create_todo_list("Books", user)

    Task.objects.create(todo_list=todo_list, name="Eggs", done=False)
    Task.objects.create(todo_list=another_todo_list, name="The seven sisters", done=False)

    url = f"/api/todo-lists/{todo_list.id}/"
    response = client.get(url)

    assert len(response.data["todo_tasks"]) == 1
    assert response.data["todo_tasks"][0] == "Eggs"


@pytest.mark.django_db
def test_update_todo_list_name(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    client = create_authenticated_client(user)

    todo_list = create_todo_list(name="Super", user=user)

    url = f"/api/todo-lists/{todo_list.id}/"

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

    url = f"/api/todo-lists/{todo_list.id}/"

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert len(TodoList.objects.all()) == 0


@pytest.mark.django_db
def test_update_todo_list_restricted_to_owner(
    create_user, django_user_model, create_authenticated_client, create_todo_list, admin_client
):
    user = create_user()
    todo_list = create_todo_list(name="Super", user=user)

    user_not_owner = User.objects.create(username="testuser", email="test@user.com", password="lksdhlka2")
    client = create_authenticated_client(user_not_owner)
    url = f"/api/todo-lists/{todo_list.id}/"
    print(url)
    data = {
        "name": "Food",
    }

    response = client.put(url, data=data, format="json")
    print(response)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_partial_update_todo_list_restricted_to_owner(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    todo_list_owner = User.objects.create_user("owner", "owner@todoapp.com", "something")
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Super", todo_list_owner)

    url = f"/api/todo-lists/{todo_list.id}/"

    data = {
        "name": "Food",
    }

    response = client.patch(url, data=data, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_todo_list_restricted_to_owner(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    todo_list_creator = User.objects.create_user("Owner", "owner@todoapp.com", "something")
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Super", todo_list_creator)

    url = f"/api/todo-lists/{todo_list.id}/"

    response = client.delete(url, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_client_retrieves_only_todo_list_of_owner(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    todo_list = create_todo_list("Super", user)

    another_user = User.objects.create(username="SomeoneElse", email="someone@else.com", password="something")
    create_todo_list("Books", another_user)

    client = create_authenticated_client(user)
    url = "/api/todo-lists/"
    response = client.get(url)

    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["name"] == "Super"


@pytest.mark.django_db
def test_admin_can_retrieve_todo_list(create_user, create_authenticated_client, create_todo_list, admin_user):

    user = create_user()
    client = create_authenticated_client(admin_user)

    todo_list = create_todo_list("Super", user, False)
    id = str(todo_list.id)

    url = f"/api/todo-lists/{id}/"

    response = client.get(url)
    print(response)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_correct_order_todo_lists(create_user, create_authenticated_client):
    url = "/api/todo-lists/"
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

    assert response.data["results"][0]["name"] == "New"
    assert response.data["results"][1]["name"] == "Old"
    assert response.data["results"][2]["name"] == "Oldest"


@pytest.mark.django_db
def test_todo_lists_order_changed_when_task_marked_done(create_user, create_authenticated_client):

    user = create_user()
    client = create_authenticated_client(user)

    more_recent_time = datetime.now() - timedelta(days=1)
    older_time = datetime.now() - timedelta(days=20)

    with mock.patch("django.utils.timezone.now") as mock_now:
        mock_now.return_value = older_time
        older_list = TodoList.objects.create(name="Older", owner=user)
        task_on_older_list = Task.objects.create(name="Milk", done=False, todo_list=older_list)

        mock_now.return_value = more_recent_time
        TodoList.objects.create(name="Recent", updated=datetime.now() - timedelta(days=100), owner=user)

    todo_task_url = f"/api/todo-lists/{older_list.id}/tasks/{task_on_older_list.id}"
    todo_lists_url = "/api/todo-lists/"

    data = {"done": True}

    client.patch(todo_task_url, data)

    response = client.get(todo_lists_url)

    assert response.data["results"][0]["name"] == "Recent"
    assert response.data["results"][1]["name"] == "Older"


@pytest.mark.django_db
def test_search_archived_todo_lists(create_user, create_authenticated_client):
    user = create_user()
    client = create_authenticated_client(user)
    TodoList.objects.create(name="Super", owner=user)
    TodoList.objects.create(name="Books", owner=user, archived=True)

    search_param = "?archived=True"
    url = reverse("filter-todo-lists") + search_param

    response = client.get(url)
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Books"


@pytest.mark.django_db
def test_search_returns_only_users_results(create_user, create_authenticated_client, create_todo_list, create_task):
    user = create_user()
    client = create_authenticated_client(user)
    another_user = User.objects.create_user("SomeOtherUser", "someother@user.com", "something")

    todo_list_1 = TodoList.objects.create(name="Books", owner=user, archived=True)
    create_task("Milk", todo_list_1)
    todo_list_2 = create_todo_list("Books", another_user)
    create_task("Milk", todo_list_2)

    search_param = "?archived=True"
    url = reverse("filter-todo-lists") + search_param

    response = client.get(url)
    assert len(response.data) == 1
