from urllib.parse import quote


def test_get_activities_returns_activity_data(client):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_adds_participant(client):
    # Arrange
    email = "newstudent@mergington.edu"
    activity_name = "Gym Class"
    encoded_activity = quote(activity_name, safe="")
    url = f"/activities/{encoded_activity}/signup?email={quote(email, safe='')}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    updated = client.get("/activities").json()
    assert email in updated[activity_name]["participants"]


def test_signup_missing_activity_returns_404(client):
    # Arrange
    email = "user@example.com"
    encoded_activity = quote("Nonexistent Club", safe="")
    url = f"/activities/{encoded_activity}/signup?email={quote(email, safe='')}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 404


def test_delete_participant_removes_participant(client):
    # Arrange
    email = "john@mergington.edu"
    activity_name = "Gym Class"
    encoded_activity = quote(activity_name, safe="")
    url = f"/activities/{encoded_activity}/participants?email={quote(email, safe='')}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 200
    updated = client.get("/activities").json()
    assert email not in updated[activity_name]["participants"]


def test_delete_missing_participant_returns_404(client):
    # Arrange
    email = "missing@mergington.edu"
    encoded_activity = quote("Gym Class", safe="")
    url = f"/activities/{encoded_activity}/participants?email={quote(email, safe='')}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 404
