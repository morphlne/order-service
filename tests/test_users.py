import pytest

from models.user import User

EMAIL_WITH_WHITESPACE = pytest.mark.parametrize(
    "email",
    [" john@example.com", "john@example.com "],
    ids=["email_starting_whitespace", "email_ending_whitespace"]
)

INVALID_EMAIL = pytest.mark.parametrize(
    "email",
    ["", "name@", "name@domain.", "@domain.com", "namedomain.com", "na me@domain.com"],
    ids=["empty_email", "email_no_domain", "email_no_top_lvl_domain",
         "email_no_local_part", "email_no_@", "email_with_space"]
)


def mock_refresh_user(user):
    user.user_id = 1
    user.is_active = True


def test_get_users_filter_inactive(client, mock_db):
    active_user = User(name="John Doe", email="john@example.com")
    active_user.user_id = 1
    active_user.is_active = True
    inactive_user = User(name="Jane Doe", email="jane@example.com")
    inactive_user.user_id = 2
    inactive_user.is_active = False

    mock_db.query.return_value.all.return_value = [active_user, inactive_user]

    response = client.get("/users")

    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 1
    assert response_data[0]["user_id"] == active_user.user_id
    assert response_data[0]["name"] == active_user.name

    mock_db.query.assert_called_once_with(User)
    mock_db.query.return_value.all.assert_called_once()


def test_get_user_show_active(client, mock_db):
    active_user = User(name="John Doe", email="john@example.com")
    active_user.user_id = 1
    active_user.is_active = True

    mock_db.query.return_value.filter.return_value.first.return_value = active_user

    response = client.get("/users/1")

    response_data = response.json()
    assert response.status_code == 200
    assert response_data["user_id"] == active_user.user_id
    assert response_data["name"] == active_user.name

    mock_db.query.assert_called_once_with(User)
    mock_db.query.return_value.filter.return_value.first.assert_called_once()


def test_get_user_filter_inactive(client, mock_db):
    inactive_user = User(name="Jane Doe", email="jane@example.com")
    inactive_user.user_id = 2
    inactive_user.is_active = False

    mock_db.query.return_value.filter.return_value.first.return_value = inactive_user

    response = client.get("/users/1")

    response_data = response.json()
    assert response.status_code == 404
    assert response_data["detail"] == "User not found"

    mock_db.query.assert_called_once_with(User)
    mock_db.query.return_value.filter.return_value.first.assert_called_once()


@EMAIL_WITH_WHITESPACE
def test_create_user_success_strip_email(client, mock_db, email):
    request = {"name": "John Doe", "email": email}

    mock_db.refresh.side_effect = mock_refresh_user

    response = client.post("/users", json=request)

    response_data = response.json()
    assert response.status_code == 200
    assert response_data["message"] == "User created"
    assert response_data["user"]["email"] == email.strip()

    created_user = mock_db.add.call_args[0][0]
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(created_user)


def test_create_user_fail_same_email(client, mock_db):
    request = {"name": "John Doe", "email": "john@example.com"}

    mock_db.refresh.side_effect = mock_refresh_user

    response = client.post("/users", json=request)

    response_data = response.json()
    assert response.status_code == 200
    assert response_data["message"] == "User created"

    request2 = {"name": "John WithSameEmail", "email": "john@example.com"}

    response2 = client.post("/users", json=request2)

    response_data2 = response2.json()
    assert response2.status_code == 400
    assert response_data2["detail"] == "User with email already exists john@example.com"


def test_create_user_fail_name_validation(client, mock_db):
    request = {"name": "", "email": "john@example.com"}

    response = client.post("/users", json=request)

    assert response.status_code == 422

    mock_db.assert_not_called()


@INVALID_EMAIL
def test_create_user_fail_email_validation(client, mock_db, email):
    request = {"name": "John Doe", "email": email}

    response = client.post("/users", json=request)

    assert response.status_code == 422

    mock_db.assert_not_called()


@EMAIL_WITH_WHITESPACE
def test_update_user_success_strip_email(client, mock_db, email):
    request = {"name": "John Doe", "email": email}

    db_user = User(name="John Doe", email="old@example.com")
    db_user.user_id = 1
    db_user.is_active = True

    mock_db.query.return_value.filter.return_value.first.return_value = db_user

    response = client.put("/users/1", json=request)

    response_data = response.json()
    assert response.status_code == 200
    assert response_data["message"] == "User updated"
    assert response_data["user"]["email"] == email.strip()

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


@INVALID_EMAIL
def test_update_user_fail_email_validation(client, mock_db, email):
    request = {"name": "John Doe", "email": email}

    response = client.put("/users/1", json=request)

    assert response.status_code == 422

    mock_db.assert_not_called()


def test_make_user_inactive_success(client, mock_db):
    request = {"is_active": "false"}

    db_user = User(name="John Doe", email="john@example.com")
    db_user.user_id = 1
    db_user.is_active = True

    mock_db.query.return_value.filter.return_value.first.return_value = db_user

    response = client.patch("/users/1", json=request)

    response_data = response.json()
    assert response.status_code == 200
    assert response_data["message"] == "User inactive"
    assert response_data["user"]["is_active"] == False

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_make_user_active_fail_not_supported(client, mock_db):
    request = {"is_active": "true"}

    response = client.patch("/users/1", json=request)

    response_data = response.json()
    assert response.status_code == 400
    assert response_data["detail"] == "User activation is not supported"

    mock_db.assert_not_called()
