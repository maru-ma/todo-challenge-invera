import pytest
from todo_app.models import User
from rest_framework.test import APIClient

from todo_app.models import TodoList, Task


@pytest.fixture(scope="session")
def create_task():
    def _create_task(name: str, todo_list: TodoList, done: bool = False):
        task = Task.objects.create(name=name, done=done, todo_list=todo_list)

        return task

    return _create_task


@pytest.fixture(scope="session")
def create_user():
    def _create_user():
        return User.objects.create_user("TestUser", "user@test.com", "blahblah")

    return _create_user


@pytest.fixture(scope="session")
def create_authenticated_client():
    def _create_authenticated_client(user: User):
        client = APIClient()
        client.force_login(user)

        return client

    return _create_authenticated_client


@pytest.fixture(scope="session")
def create_todo_list():
    def _create_todo_list(name: str, user: User, archived: bool = False):
        todo_list = TodoList.objects.create(name=name, owner=user, archived=archived)

        return todo_list

    return _create_todo_list
