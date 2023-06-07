import pytest
from rest_framework.test import APIClient

from todo_app.models import Task, TodoList, User


@pytest.fixture(scope="session")
def create_task():
    """
    Fixture for creating a task.
    Usage: create_task(name: str, todo_list: TodoList, done: bool = False) -> Task
    """

    def _create_task(name: str, todo_list: TodoList, done: bool = False):
        return Task.objects.create(name=name, done=done, todo_list=todo_list)

    return _create_task


@pytest.fixture(scope="session")
def create_user():
    """
    Fixture for creating a user.
    Usage: create_user() -> User
    """

    def _create_user():
        return User.objects.create_user("TestUser", "user@test.com", "blahblah")

    return _create_user


@pytest.fixture(scope="session")
def create_authenticated_client():
    """
    Fixture for creating an authenticated APIClient.
    Usage: create_authenticated_client(user: User) -> APIClient
    """

    def _create_authenticated_client(user: User):
        client = APIClient()
        client.force_login(user)

        return client

    return _create_authenticated_client


@pytest.fixture(scope="session")
def create_todo_list():
    """
    Fixture for creating a todo list.
    Usage: create_todo_list(name: str, user: User, archived: bool = False) -> TodoList
    """

    def _create_todo_list(name: str, user: User, archived: bool = False):
        return TodoList.objects.create(name=name, owner=user, archived=archived)

    return _create_todo_list
