import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (nothing to set up, just use the client)
    
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser1@mergington.edu"
    # Clean up in case already present
    client.delete(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Clean up
    client.delete(f"/activities/{activity}/signup?email={email}")

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    client.delete(f"/activities/{activity}/signup?email={email}")
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    client.delete(f"/activities/{activity}/signup?email={email}")

def test_signup_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "testuser3@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser4@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]

def test_unregister_not_registered():
    # Arrange
    activity = "Chess Club"
    email = "testuser5@mergington.edu"
    client.delete(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]

def test_unregister_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "testuser6@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
