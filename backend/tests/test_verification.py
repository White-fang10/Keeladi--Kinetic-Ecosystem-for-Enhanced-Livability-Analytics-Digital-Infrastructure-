from app.core.config import settings
from tests.test_complaints import get_auth_token

def setup_mock_task(db_session, worker_id):
    from app.models.complaint import Complaint
    from app.models.task import Task
    complaint = Complaint(
        reference_number="KLD-VERIF-123",
        user_id="citizen-id",
        ward_id="mock-ward-id",
        title="Verif Complaint",
        category="OTHER",
        latitude=13.0,
        longitude=80.0
    )
    db_session.add(complaint)
    db_session.commit()
    db_session.refresh(complaint)
    
    task = Task(
        complaint_id=complaint.id,
        worker_id=worker_id,
        assigned_by="assigner-id",
        status="ASSIGNED"
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task

def test_submit_before_verification(client, db_session):
    headers = get_auth_token(client, email="worker@keeladi.gov", password="password")
    
    from app.models.user import User
    user = db_session.query(User).filter(User.email == "worker@keeladi.gov").first()
    user.role = "SANITATION_WORKER"
    db_session.commit()
    
    task = setup_mock_task(db_session, user.id)
    
    payload = {
        "task_id": task.id,
        "before_image_url": "http://example.com/before.jpg",
        "before_lat": 13.0001,
        "before_lng": 80.0001
    }
    
    response = client.post(f"{settings.API_V1_STR}/verification/before", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["location_verified"] is True  # Should be close enough to 13.0, 80.0
