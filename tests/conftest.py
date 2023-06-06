import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from todo_app.models import TodoList, Item


@pytest.fixture(scope="session")
def create_item():
    def _create_item(name, todo_list):
        item = Item.objects.create(name=name, done=False, todo_list=todo_list)

        return item

    return _create_item


@pytest.fixture(scope="session")
def create_user():
    def _create_user():
        return User.objects.create_user("TestUser", "user@test.com", "blahblah")

    return _create_user


@pytest.fixture(scope="session")
def create_authenticated_client():
    def _create_authenticated_client(user):
        client = APIClient()
        client.force_login(user)

        return client

    return _create_authenticated_client


@pytest.fixture(scope="session")
def create_todo_list():
    def _create_todo_list(name, user):
        todo_list = TodoList.objects.create(name=name, owner=user)

        return todo_list

    return _create_todo_list
