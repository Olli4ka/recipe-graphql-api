import pytest
from django.test import Client
from graphql_jwt.shortcuts import get_token

from .factories import UserFactory


@pytest.fixture
def graphql_client():
    return Client()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def owner():
    return UserFactory()


@pytest.fixture
def intruder():
    return UserFactory()


@pytest.fixture
def authenticated_graphql_client(user):
    client = Client()

    token = get_token(user)

    client.defaults["HTTP_AUTHORIZATION"] = f"JWT {token}"

    return client


@pytest.fixture
def authenticated_client(graphql_client):
    def _authenticate(user):
        token = get_token(user)

        graphql_client.defaults["HTTP_AUTHORIZATION"] = f"JWT {token}"

        return graphql_client

    return _authenticate
