import pytest

from .factories import UserFactory


@pytest.mark.django_db
def test_token_auth_success(graphql_client):
    user = UserFactory(
        username="testuser",
        password="password123",
    )

    mutation = """
    mutation {
      tokenAuth(
        username: "testuser"
        password: "password123"
      ) {
        token
      }
    }
    """

    response = graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" not in data

    token = data["data"]["tokenAuth"]["token"]

    assert token
    assert isinstance(token, str)


@pytest.mark.django_db
def test_token_auth_invalid_password(graphql_client):
    UserFactory(
        username="testuser",
        password="password123",
    )

    mutation = """
    mutation {
      tokenAuth(
        username: "testuser"
        password: "wrongpassword"
      ) {
        token
      }
    }
    """

    response = graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" in data
    assert data["data"]["tokenAuth"] is None
    assert data["errors"][0]["message"] == "Please enter valid credentials"


@pytest.mark.django_db
def test_token_auth_nonexistent_user(graphql_client):
    mutation = """
    mutation {
      tokenAuth(
        username: "doesnotexist"
        password: "password123"
      ) {
        token
      }
    }
    """

    response = graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" in data
    assert data["data"]["tokenAuth"] is None
    assert data["errors"][0]["message"] == ("Please enter valid credentials")


@pytest.mark.django_db
def test_verify_token_success(graphql_client):
    UserFactory(
        username="testuser",
        password="password123",
    )

    login_mutation = """
    mutation {
      tokenAuth(
        username: "testuser"
        password: "password123"
      ) {
        token
      }
    }
    """

    login_response = graphql_client.post(
        "/graphql/",
        data={"query": login_mutation},
        content_type="application/json",
    )

    login_data = login_response.json()

    assert "errors" not in login_data

    token = login_data["data"]["tokenAuth"]["token"]

    verify_mutation = f"""
    mutation {{
      verifyToken(
        token: "{token}"
      ) {{
        payload
      }}
    }}
    """

    verify_response = graphql_client.post(
        "/graphql/",
        data={"query": verify_mutation},
        content_type="application/json",
    )

    verify_data = verify_response.json()

    assert verify_response.status_code == 200
    assert "errors" not in verify_data
    assert verify_data["data"]["verifyToken"]["payload"]


@pytest.mark.django_db
def test_verify_token_invalid(graphql_client):
    mutation = """
    mutation {
      verifyToken(
        token: "this-is-not-a-valid-jwt"
      ) {
        payload
      }
    }
    """

    response = graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" in data
    assert data["data"]["verifyToken"] is None


@pytest.mark.django_db
def test_refresh_token_success(graphql_client):
    UserFactory(
        username="testuser",
        password="password123",
    )

    login_mutation = """
    mutation {
      tokenAuth(
        username: "testuser"
        password: "password123"
      ) {
        token
      }
    }
    """

    login_response = graphql_client.post(
        "/graphql/",
        data={"query": login_mutation},
        content_type="application/json",
    )

    login_data = login_response.json()

    assert "errors" not in login_data

    token = login_data["data"]["tokenAuth"]["token"]

    refresh_mutation = f"""
    mutation {{
      refreshToken(
        token: "{token}"
      ) {{
        token
      }}
    }}
    """

    refresh_response = graphql_client.post(
        "/graphql/",
        data={"query": refresh_mutation},
        content_type="application/json",
    )

    refresh_data = refresh_response.json()

    assert refresh_response.status_code == 200
    assert "errors" not in refresh_data

    new_token = refresh_data["data"]["refreshToken"]["token"]

    assert new_token
    assert isinstance(new_token, str)


@pytest.mark.django_db
def test_refresh_token_invalid(graphql_client):
    mutation = """
    mutation {
      refreshToken(
        token: "this-is-not-a-valid-jwt"
      ) {
        token
      }
    }
    """

    response = graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" in data
    assert data["data"]["refreshToken"] is None
