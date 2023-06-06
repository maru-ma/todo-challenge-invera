import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from todo_app.models import User


@pytest.mark.django_db
def test_call_with_token_authentication(create_user):
    username = "GirlThatLovesToCode"
    password = "something"
    User.objects.create_user(username, password=password)

    client = APIClient()
    token_url = reverse("api_token_auth")

    data = {"username": username, "password": password}

    token_response = client.post(token_url, data, format="json")
    token = token_response.data["token"]

    url = reverse("all-todo-lists")
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
