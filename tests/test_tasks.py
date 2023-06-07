import pytest
from django.urls import reverse
from rest_framework import status

from todo_app.models import User, Task


@pytest.mark.django_db
def test_valid_task_is_created(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    todo_list = create_todo_list("Study", user)

    url = reverse("list-add-tasks", args=[todo_list.id])

    data = {"name": "AWS", "done": False}
    client = create_authenticated_client(user)
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_task_missing_data_returns_bad_request(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    todo_list = create_todo_list("Study", user)

    url = reverse("list-add-tasks", args=[todo_list.id])

    data = {
        "done": "False",
    }
    client = create_authenticated_client(user)
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_task_is_retrieved_by_id(create_user, create_authenticated_client, create_todo_list, create_task):
    user = create_user()
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Super", user)
    task = create_task("Chocolate", todo_list)

    url = reverse("task-detail", kwargs={"pk": task.todo_list.id, "task_pk": task.id})

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Chocolate"


@pytest.mark.django_db
def test_update_task_done_status(create_user, create_authenticated_client, create_todo_list, create_task):
    user = create_user()
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Study", user)
    task = create_task("AWS", todo_list)

    url = reverse("task-detail", kwargs={"pk": todo_list.id, "task_pk": task.id})

    data = {"name": "AWS", "done": True}
    response = client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert Task.objects.get().done is True


@pytest.mark.django_db
def test_update_task_done_status_with_missing_data_returns_bad_request(
    create_user, create_authenticated_client, create_todo_list, create_task
):
    user = create_user()
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Study", user)
    task = create_task("AWS", todo_list)

    url = reverse("task-detail", kwargs={"pk": todo_list.id, "task_pk": task.id})

    data = {"adse": True}
    response = client.put(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_task_name_with_partial_update(create_user, create_authenticated_client, create_todo_list, create_task):
    user = create_user()
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Study", user)
    task = create_task("AWS", todo_list)

    url = reverse("task-detail", kwargs={"pk": todo_list.id, "task_pk": task.id})

    data = {"name": "Docker"}
    response = client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert Task.objects.get().name == "Docker"


@pytest.mark.django_db
def test_not_owner_of_list_can_not_add_task(create_user, create_authenticated_client, create_todo_list):
    user = create_user()
    client = create_authenticated_client(user)

    todo_list_owner = User.objects.create_user("Creator", "creator@list.com", "something")
    todo_list = create_todo_list("Super", todo_list_owner)

    url = reverse("list-add-tasks", args=[todo_list.id])

    data = {"name": "Milk", "done": False}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_add_tasks(create_user, create_todo_list, admin_client):
    user = create_user()
    todo_list = create_todo_list("Super", user)

    url = reverse("list-add-tasks", kwargs={"pk": todo_list.id})

    data = {"name": "Milk", "done": False}

    response = admin_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_task_detail_access_restricted_if_not_owner_of_todo_list(
    create_user, create_authenticated_client, create_todo_list, create_task
):
    user = create_user()
    todo_list_owner = User.objects.create_user("Owner", "owner@todolist.com", "something")
    todo_list = create_todo_list("Super", todo_list_owner)
    client = create_authenticated_client(user)
    task = create_task("Chocolate", todo_list)

    url = reverse("task-detail", kwargs={"pk": task.todo_list.id, "task_pk": task.id})

    response = client.get(url, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_task_update_restricted_if_not_owner_of_todo_list(
    create_user, create_authenticated_client, create_todo_list, create_task
):
    user = create_user()
    todo_list_owner = User.objects.create_user("Creator", "creator@list.com", "something")
    todo_list = create_todo_list("Super", todo_list_owner)
    client = create_authenticated_client(user)
    task = create_task("Chocolate", todo_list)

    url = reverse("task-detail", kwargs={"pk": task.todo_list.id, "task_pk": task.id})

    data = {"name": "Chocolate", "done": True}

    response = client.put(url, data=data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_task_partial_update_restricted_if_not_owner_of_todo_list(
    create_user, create_authenticated_client, create_todo_list, create_task
):
    user = create_user()
    todo_list_owner = User.objects.create_user("Creator", "creator@list.com", "something")
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Super", todo_list_owner)

    task = create_task("Chocolate", todo_list)

    url = reverse("task-detail", kwargs={"pk": task.todo_list.id, "task_pk": task.id})

    data = {"done": True}

    response = client.patch(url, data=data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_task_delete_restricted_if_not_owner_of_todo_list(
    create_user, create_authenticated_client, create_todo_list, create_task
):
    user = create_user()
    todo_list_owner = User.objects.create_user("Creator", "creator@list.com", "something")
    client = create_authenticated_client(user)
    todo_list = create_todo_list("Super", todo_list_owner)
    task = create_task("Chocolate", todo_list)

    url = reverse("task-detail", kwargs={"pk": task.todo_list.id, "task_pk": task.id})

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_retrieve_single_task(create_user, create_task, create_todo_list, admin_client):
    user = create_user()
    todo_list = create_todo_list("Super", user)
    task = create_task("Milk", todo_list)

    url = reverse("task-detail", kwargs={"pk": task.todo_list.id, "task_pk": task.id})

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_tasks_is_retrieved_by_todo_list_member(
    create_user, create_authenticated_client, create_todo_list, create_task
):
    user = create_user()
    todo_list = create_todo_list("Fruits", user)
    task_1 = create_task("Orange", todo_list)
    task_2 = create_task("Apples", todo_list)

    client = create_authenticated_client(user)
    url = reverse("list-add-tasks", kwargs={"pk": todo_list.id})
    response = client.get(url)

    assert len(response.data["results"]) == 2
    assert response.data["results"][0]["name"] == task_1.name
    assert response.data["results"][1]["name"] == task_2.name


@pytest.mark.django_db
def test_not_owner_can_not_retrieve_tasks(create_user, create_authenticated_client, create_task, create_todo_list):
    user_1 = create_user()
    todo_list = create_todo_list("First List", user_1)

    task = create_task("Milk", todo_list)

    user = User.objects.create_user("TestUser2", "user2@test.com", "blahblah2")
    client = create_authenticated_client(user)
    url = reverse("list-add-tasks", kwargs={"pk": task.todo_list.id})

    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_list_tasks_only_the_ones_belonging_to_the_same_todo_list(
    create_user, create_authenticated_client, create_todo_list, create_task
):
    user = create_user()

    todo_list = create_todo_list("First List", user)
    task_from_this_list = create_task("Oranges", todo_list)

    another_todo_list = create_todo_list("Another list!", user)
    task_from_another_list = create_task("Apples", another_todo_list)

    client = create_authenticated_client(user)
    url = reverse("list-add-tasks", kwargs={"pk": todo_list.id})

    response = client.get(url)

    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["name"] == task_from_this_list.name


@pytest.mark.django_db
def test_duplicate_task_on_list_bad_request(create_user, create_authenticated_client, create_todo_list, create_task):
    user = create_user()
    client = create_authenticated_client(user)

    todo_list = create_todo_list("Super", user)
    task = create_task("Milk", todo_list)

    url = reverse("list-add-tasks", args=[todo_list.id])
    data = {"name": "Milk", "done": False}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(todo_list.todo_tasks.all()) == 1


@pytest.mark.django_db
def test_filter_done_tasks(create_user, create_authenticated_client, create_todo_list, create_task):
    user = create_user()
    client = create_authenticated_client(user)

    todo_list = create_todo_list("Super", user)
    undone_task = create_task("Eggs", todo_list)
    done_task = create_task("Milk", todo_list, True)

    search_param = "?done=True"
    url = reverse("filter-tasks", kwargs={"pk": todo_list.id}) + search_param

    response = client.get(url)
    assert len(response.data) == 1
    assert response.data[0]["name"] == done_task.name


@pytest.mark.django_db
def test_filter_undone_tasks(create_user, create_authenticated_client, create_todo_list, create_task):
    user = create_user()
    client = create_authenticated_client(user)

    todo_list = create_todo_list("Super", user)
    undone_task = create_task("Eggs", todo_list)
    done_task = create_task("Milk", todo_list, True)

    search_param = "?done=False"
    url = reverse("filter-tasks", kwargs={"pk": todo_list.id}) + search_param

    response = client.get(url)
    assert len(response.data) == 1
    assert response.data[0]["name"] == undone_task.name
