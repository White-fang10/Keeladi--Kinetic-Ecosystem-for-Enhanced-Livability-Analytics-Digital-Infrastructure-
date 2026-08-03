from app.core.config import settings
from tests.test_complaints import get_auth_token

def test_assign_new_task(client, db_session):
    """Test assigning a new task to a worker."""
    headers = get_auth_token(client, email="junior.engineer@keeladi.gov", password="password")
    
    # We need to manually set this user's role to JUNIOR_ENGINEER in the DB
    from app.models.user import User
    user = db_session.query(User).filter(User.email == "junior.engineer@keeladi.gov").first()
    user.role = "SUPERVISOR"
    db_session.commit()
    
    # First, create a mock complaint directly in the DB to associate with the task
    from app.models.complaint import Complaint
    complaint = Complaint(
        reference_number="KLD-MOCK-123",
        user_id=user.id,
        ward_id="mock-ward-id",
        title="Mock Complaint",
        category="OTHER",
        latitude=0.0,
        longitude=0.0,
        citizen_name="Mock Citizen",
        citizen_phone="1234567890"
    )
    db_session.add(complaint)
    db_session.commit()
    db_session.refresh(complaint)
    
    payload = {
        "complaint_id": complaint.id,
        "worker_id": "mock-worker-id",
        "priority": "HIGH",
        "notes": "Please fix this quickly."
    }
    
    response = client.post(f"{settings.API_V1_STR}/tasks", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "ASSIGNED"
    
    # Verify complaint status was updated
    db_session.refresh(complaint)
    assert complaint.status == "ASSIGNED"
