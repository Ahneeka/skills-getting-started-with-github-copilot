from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_rejects_duplicate_registration():
    # Arrange
    activity = "Chess Club"
    email = "duplicate@example.edu"

    # Act
    first_signup = client.post(f"/activities/{activity}/signup?email={email}")
    second_signup = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert first_signup.status_code == 200, first_signup.text
    assert second_signup.status_code == 400, second_signup.text
    assert second_signup.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant_from_activity():
    # Arrange
    activity = "Soccer Club"
    email = "student@example.edu"

    # Act
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    delete_response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert signup_response.status_code == 200, signup_response.text
    assert delete_response.status_code == 200, delete_response.text
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_rejects_missing_participant():
    # Arrange
    activity = "Programming Class"
    email = "missing@example.edu"

    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 404, response.text
