from app.core.config import settings
from tests.test_complaints import get_auth_token

def test_register_vehicle(client, db_session):
    """Test registering a new vehicle."""
    headers = get_auth_token(client, email="exec.engineer@keeladi.gov", password="password")
    
    from app.models.user import User
    user = db_session.query(User).filter(User.email == "exec.engineer@keeladi.gov").first()
    user.role = "ADMIN"
    db_session.commit()
    
    payload = {
        "registration_number": "TN-01-AB-1234",
        "vehicle_type": "COMPACTOR",
        "capacity_kg": 5000.0,
        "ward_id": "mock-ward-id"
    }
    
    response = client.post(f"{settings.API_V1_STR}/vehicles", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["registration_number"] == "TN-01-AB-1234"
    assert data["data"]["status"] == "AVAILABLE"

def test_update_vehicle_status(client, db_session):
    """Test driver updating vehicle status."""
    headers = get_auth_token(client, email="driver@keeladi.gov", password="password")
    
    from app.models.user import User
    user = db_session.query(User).filter(User.email == "driver@keeladi.gov").first()
    user.role = "WORKER"
    db_session.commit()
    
    # Create a mock vehicle
    from app.models.vehicle import Vehicle
    vehicle = Vehicle(
        registration_number="TN-02-XY-9999",
        vehicle_type="TIPPER",
        capacity_kg=2000.0,
        ward_id="mock-ward-id",
        status="AVAILABLE"
    )
    db_session.add(vehicle)
    db_session.commit()
    db_session.refresh(vehicle)
    
    payload = {
        "status": "FULL"
    }
    
    response = client.patch(f"{settings.API_V1_STR}/vehicles/{vehicle.id}/status", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "FULL"
