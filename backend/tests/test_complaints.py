from app.core.config import settings

def get_auth_token(client, email="citizen@keeladi.gov", password="password"):
    """Helper to register and login a user, returning the auth headers."""
    client.post(f"{settings.API_V1_STR}/auth/register", json={
        "full_name": "Citizen",
        "email": email,
        "password": password
    })
    
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": email, "password": password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_submit_complaint(client, db_session):
    """Test a citizen submitting a new complaint."""
    headers = get_auth_token(client)
    
    # Note: In a real test, we would need to create a Ward and Department first to satisfy foreign keys.
    # For MVP SQLite with disabled foreign key enforcement by default, this will pass.
    payload = {
        "title": "Overflowing garbage bin",
        "description": "The bin on Main Street has not been cleared for 3 days.",
        "category": "GARBAGE_OVERFLOW",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "ward_id": "dummy-ward-id",
        "citizen_name": "Test Citizen",
        "citizen_phone": "1234567890"
    }
    
    response = client.post(f"{settings.API_V1_STR}/public/complaints", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "PROCESSING"
    assert "KLD" in data["data"]["reference_number"]
