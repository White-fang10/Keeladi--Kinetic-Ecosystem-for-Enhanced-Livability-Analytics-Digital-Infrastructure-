# Import all models so SQLAlchemy Base.metadata knows about them
from app.models.user import User
from app.models.complaint import Complaint, ComplaintImage, ComplaintHistory
from app.models.task import Task
from app.models.vehicle import Vehicle, VehicleLocation, CollectionRecord
from app.models.verification import Verification
from app.models.notification import Notification
from app.models.prediction import PredictionResult, WasteCollectionHistory
from app.models.department import Department
from app.models.ward import Ward
from app.models.upload import Upload
from app.models.enums import (
    UserRole, UserStatus, ComplaintCategory, ComplaintStatus,
    Priority, TaskStatus, VehicleType, VehicleStatus, ApprovalStatus,
)
