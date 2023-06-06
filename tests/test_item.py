import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from todo_app.models import Item, TodoList


@pytest.mark.django_db
def test_item_is_retrieved_by_id(create_user, create_authenticated_client, create_todo_list, create_item):
    user = create_user()
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Super", user)
    item = create_item("Chocolate", todo_list)

    url = reverse("item-detail", kwargs={"pk": item.todo_list.id, "item_pk": item.id})

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Chocolate"


@pytest.mark.django_db
def test_not_owner_of_list_can_not_add_item(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    client = create_authenticated_client(user)

    todo_list_owner = User.objects.create_user("Creator", "creator@list.com", "something")
    todo_list = create_todo_list("Super", todo_list_owner)

    url = reverse("list-add-items", args=[todo_list.id])

    data = {"name": "Milk", "done": False}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_add_items(create_user, create_todo_list, admin_client):
    user = create_user()
    todo_list = create_todo_list("Super", user)

    url = reverse("list-add-items", kwargs={"pk": todo_list.id})

    data = {"name": "Milk", "done": False}

    response = admin_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_item_detail_access_restricted_if_not_owner_of_todo_list(
    create_user, create_authenticated_client, create_todo_list, create_item
):
    user = create_user()
    todo_list_owner = User.objects.create_user("Owner", "owner@todolist.com", "something")
    todo_list = create_todo_list("Super", todo_list_owner)
    client = create_authenticated_client(user)
    item = create_item("Chocolate", todo_list)

    url = reverse("item-detail", kwargs={"pk": item.todo_list.id, "item_pk": item.id})

    response = client.get(url, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_item_update_restricted_if_not_owner_of_todo_list(
    create_user, create_authenticated_client, create_todo_list, create_item
):
    user = create_user()
    todo_list_owner = User.objects.create_user("Creator", "creator@list.com", "something")
    todo_list = create_todo_list("Super", todo_list_owner)
    client = create_authenticated_client(user)
    item = create_item("Chocolate", todo_list)

    url = reverse("item-detail", kwargs={"pk": item.todo_list.id, "item_pk": item.id})

    data = {"name": "Chocolate", "done": True}

    response = client.put(url, data=data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_item_partial_update_restricted_if_not_owner_of_todo_list(
    create_user, create_authenticated_client, create_todo_list, create_item
):
    user = create_user()
    todo_list_owner = User.objects.create_user("Creator", "creator@list.com", "something")
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Super", todo_list_owner)

    item = create_item("Chocolate", todo_list)

    url = reverse("item-detail", kwargs={"pk": item.todo_list.id, "item_pk": item.id})

    data = {"done": True}

    response = client.patch(url, data=data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_item_delete_restricted_if_not_owner_of_todo_list(
    create_user, create_authenticated_client, create_todo_list, create_item
):
    user = create_user()
    todo_list_owner = User.objects.create_user("Creator", "creator@list.com", "something")
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Super", todo_list_owner)
    item = create_item("Chocolate", todo_list)

    url = reverse("item-detail", kwargs={"pk": item.todo_list.id, "item_pk": item.id})

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_retrieve_single_item(create_user, create_item, create_todo_list, admin_client):
    user = create_user()
    todo_list = create_todo_list("Super", user)
    item = create_item("Milk", todo_list)

    url = reverse("item-detail", kwargs={"pk": item.todo_list.id, "item_pk": item.id})

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_items_is_retrieved_by_todo_list_member(
    create_user, create_authenticated_client, create_todo_list, create_item
):
    user = create_user()
    todo_list = create_todo_list("Fruits", user)
    item_1 = create_item("Orange", todo_list)
    item_2 = create_item("Apples", todo_list)

    client = create_authenticated_client(user)
    url = reverse("list-add-items", kwargs={"pk": todo_list.id})
    response = client.get(url)

    assert len(response.data["results"]) == 2
    assert response.data["results"][0]["name"] == item_1.name
    assert response.data["results"][1]["name"] == item_2.name


@pytest.mark.django_db
def test_not_owner_can_not_retrieve_items(create_user, create_authenticated_client, create_item, create_todo_list):
    user_1 = create_user()
    todo_list = create_todo_list("First List", user_1)

    item = create_item("Milk", todo_list)

    user = User.objects.create_user("TestUser2", "user2@test.com", "blahblah2")
    client = create_authenticated_client(user)
    url = reverse("list-add-items", kwargs={"pk": item.todo_list.id})

    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_list_items_only_the_ones_belonging_to_the_same_todo_list(
    create_user, create_authenticated_client, create_todo_list, create_item
):
    user = create_user()

    todo_list = create_todo_list("First List", user)
    item_from_this_list = create_item("Oranges", todo_list)

    another_todo_list = create_todo_list("Another list!", user)
    item_from_another_list = create_item("Apples", another_todo_list)

    client = create_authenticated_client(user)
    url = reverse("list-add-items", kwargs={"pk": todo_list.id})

    response = client.get(url)

    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["name"] == item_from_this_list.name


@pytest.mark.django_db
def test_duplicate_item_on_list_bad_request(create_user, create_authenticated_client, create_todo_list, create_item):

    user = create_user()
    client = create_authenticated_client(user)

    todo_list = create_todo_list("Super", user)
    item = create_item("Milk", todo_list)

    url = reverse("list-add-items", args=[todo_list.id])

    data = {"name": "Milk", "done": False}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(todo_list.todo_items.all()) == 1
