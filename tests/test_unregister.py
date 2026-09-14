from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_removes_participant_from_activity():
    activity = "Chess Club"
    email = "student@example.edu"

    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200, response.text

    delete_response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert delete_response.status_code == 200, delete_response.text
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_rejects_missing_participant():
    activity = "Programming Class"
    email = "missing@example.edu"

    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404, response.text
