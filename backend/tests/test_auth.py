from app.core.config import settings

def test_health_check(client):
    """Verify that the core API is alive."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "project": settings.PROJECT_NAME, "version": "2.0.0"}

def test_register_citizen(client):
    """Test citizen registration flow."""
    payload = {
        "full_name": "Test Citizen",
        "email": "test@keeladi.gov",
        "phone": "9876543210",
        "password": "securepassword123"
    }
    response = client.post(f"{settings.API_V1_STR}/auth/register", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "test@keeladi.gov"
    assert data["data"]["role"] == "CITIZEN"

def test_login_success(client):
    """Test login to receive JWT."""
    # Register first
    client.post(f"{settings.API_V1_STR}/auth/register", json={
        "full_name": "Login Test",
        "email": "login@keeladi.gov",
        "password": "password123"
    })
    
    # Attempt login using OAuth2 Form format
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "login@keeladi.gov", "password": "password123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
