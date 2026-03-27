import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    # Arrange: pick an activity and a new email
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Remove if already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    # Cleanup
    activities[activity]["participants"].remove(email)

def test_signup_duplicate():
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_full():
    activity = "Chess Club"
    # Fill up the activity
    max_participants = activities[activity]["max_participants"]
    activities[activity]["participants"] = [f"user{i}@mergington.edu" for i in range(max_participants)]
    email = "overflow@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]
    # Cleanup
    activities[activity]["participants"] = activities[activity]["participants"][:2]

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
