from app.core.config import settings
from tests.test_complaints import get_auth_token

def test_get_and_read_notifications(client, db_session):
    headers = get_auth_token(client, email="notif@keeladi.gov", password="password")
    
    from app.models.user import User
    user = db_session.query(User).filter(User.email == "notif@keeladi.gov").first()
    
    from app.models.notification import Notification
    notif = Notification(
        user_id=user.id,
        type="SYSTEM",
        title="Test Alert",
        message="This is a test notification."
    )
    db_session.add(notif)
    db_session.commit()
    db_session.refresh(notif)
    
    # Get all notifications
    response = client.get(f"{settings.API_V1_STR}/notifications", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) > 0
    assert data["data"][0]["is_read"] is False
    
    # Mark as read
    response = client.patch(f"{settings.API_V1_STR}/notifications/{notif.id}/read", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["is_read"] is True
