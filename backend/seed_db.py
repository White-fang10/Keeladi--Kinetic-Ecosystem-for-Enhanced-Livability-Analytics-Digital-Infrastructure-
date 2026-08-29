import os
import sys
import uuid
from datetime import datetime, timedelta
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.base_class import Base
from app.db.session import engine
from app.models.user import User
from app.models.department import Department
from app.models.ward import Ward
from app.models.vehicle import Vehicle
from app.models.complaint import Complaint, ComplaintHistory
from app.models.task import Task
from app.models.verification import Verification
from app.core.security import get_password_hash
from app.models.enums import (
    UserRole, ComplaintCategory, ComplaintStatus, Priority,
    TaskStatus, VehicleType, VehicleStatus
)

def seed():
    db: Session = SessionLocal()
    try:
        # --- Clear existing data in correct dependency order ---
        print("Clearing existing data...")
        db.query(Verification).delete()
        db.query(ComplaintHistory).delete()
        db.query(Task).delete()
        db.query(Complaint).delete()
        db.query(Vehicle).delete()
        db.query(User).delete()
        db.query(Ward).delete()
        db.query(Department).delete()
        db.commit()
        print("Existing data cleared.")

        # --- Department ---
        print("Seeding department...")
        dept = Department(
            id="dept-001",
            name="Keeladi Panchayat Sanitation Department",
            code="KPSD",
            type="DISTRICT",
        )
        db.add(dept)
        db.commit()

        # --- Wards ---
        print("Seeding wards...")
        wards_data = [
            ("ward-1", "Ward 1 - Keeladi North",    "KLD-W1", 9.9312, 78.2196),
            ("ward-2", "Ward 2 - Keeladi South",    "KLD-W2", 9.9280, 78.2210),
            ("ward-3", "Ward 3 - Keeladi East",     "KLD-W3", 9.9330, 78.2250),
            ("ward-4", "Ward 4 - Keeladi West",     "KLD-W4", 9.9295, 78.2160),
            ("ward-5", "Ward 5 - Keeladi Central",  "KLD-W5", 9.9310, 78.2220),
        ]
        for wid, wname, wcode, lat, lng in wards_data:
            db.add(Ward(
                id=wid, name=wname, code=wcode,
                department_id="dept-001",
                center_lat=lat, center_lng=lng,
                area_sq_km=round(random.uniform(1.5, 4.5), 2),
                population=random.randint(2000, 8000)
            ))
        db.commit()

        # --- Users ---
        print("Seeding users...")
        users = [
            User(id="user-admin",    email="admin@keeladi.gov",             password_hash=get_password_hash("password"), full_name="Admin Officer",      role=UserRole.ADMIN,             status="ACTIVE"),
            User(id="user-je1",      email="je.kumar@keeladi.gov",          password_hash=get_password_hash("password"), full_name="Kumar JE",           role=UserRole.JUNIOR_ENGINEER,   status="ACTIVE"),
            User(id="user-sup1",     email="supervisor@keeladi.gov",        password_hash=get_password_hash("password"), full_name="Rajan Supervisor",    role=UserRole.SUPERVISOR,        status="ACTIVE"),
            User(id="user-driver1",  email="driver1@keeladi.gov",           password_hash=get_password_hash("password"), full_name="Murugan Driver",      role=UserRole.DRIVER,            status="ACTIVE"),
            User(id="user-driver2",  email="driver2@keeladi.gov",           password_hash=get_password_hash("password"), full_name="Selvam Driver",       role=UserRole.DRIVER,            status="ACTIVE"),
            User(id="user-worker1",  email="sanitation.worker@keeladi.gov", password_hash=get_password_hash("password"), full_name="Sam Sanitation",      role=UserRole.SANITATION_WORKER, status="ACTIVE"),
            User(id="user-worker2",  email="worker2@keeladi.gov",           password_hash=get_password_hash("password"), full_name="Priya Cleaner",       role=UserRole.SANITATION_WORKER, status="ACTIVE"),
            User(id="user-citizen1", email="john.doe@keeladi.gov",          password_hash=get_password_hash("password"), full_name="John Doe",            role=UserRole.CITIZEN,           status="ACTIVE"),
            User(id="user-citizen2", email="priya.s@keeladi.gov",           password_hash=get_password_hash("password"), full_name="Priya Selvam",        role=UserRole.CITIZEN,           status="ACTIVE"),
            User(id="user-citizen3", email="raman.m@keeladi.gov",           password_hash=get_password_hash("password"), full_name="Raman Murugavel",     role=UserRole.CITIZEN,           status="ACTIVE"),
        ]
        db.add_all(users)
        db.commit()

        # --- Vehicles ---
        print("Seeding vehicles...")
        vehicles = [
            Vehicle(id="veh-001", registration_number="TN58AB1234", vehicle_type=VehicleType.COMPACTOR,   capacity_kg=3000, ward_id="ward-1", driver_id="user-driver1", status=VehicleStatus.COLLECTING, make_model="Tata 407",       year=2021),
            Vehicle(id="veh-002", registration_number="TN58CD5678", vehicle_type=VehicleType.TIPPER,      capacity_kg=5000, ward_id="ward-2", driver_id="user-driver2", status=VehicleStatus.AVAILABLE,  make_model="Ashok Leyland",  year=2022),
            Vehicle(id="veh-003", registration_number="TN58EF9012", vehicle_type=VehicleType.AUTO_TIPPER, capacity_kg=800,  ward_id="ward-3", driver_id=None,           status=VehicleStatus.MAINTENANCE, make_model="Mahindra Alfa", year=2020),
            Vehicle(id="veh-004", registration_number="TN58GH3456", vehicle_type=VehicleType.MINI_TRUCK,  capacity_kg=1500, ward_id="ward-4", driver_id="user-driver1", status=VehicleStatus.FULL,        make_model="TATA ACE",      year=2023),
            Vehicle(id="veh-005", registration_number="TN58IJ7890", vehicle_type=VehicleType.COMPACTOR,   capacity_kg=3500, ward_id="ward-5", driver_id="user-driver2", status=VehicleStatus.AVAILABLE,  make_model="Tata 407",       year=2022),
            Vehicle(id="veh-006", registration_number="TN58KL2345", vehicle_type=VehicleType.TIPPER,      capacity_kg=4500, ward_id="ward-1", driver_id=None,           status=VehicleStatus.AVAILABLE,  make_model="Ashok Leyland",  year=2019),
        ]
        db.add_all(vehicles)
        db.commit()

        # --- Complaints ---
        print("Seeding complaints...")
        now = datetime.utcnow()
        complaints_data = [
            ("comp-001", "user-citizen1", "ward-1", "Overflowing dustbin near market",     ComplaintCategory.GARBAGE_OVERFLOW, ComplaintStatus.RESOLVED,    Priority.HIGH,     now - timedelta(days=7),  9.9312, 78.2196),
            ("comp-002", "user-citizen1", "ward-2", "Illegal dumping on roadside",          ComplaintCategory.ILLEGAL_DUMPING,  ComplaintStatus.IN_PROGRESS, Priority.CRITICAL, now - timedelta(days=5),  9.9280, 78.2210),
            ("comp-003", "user-citizen2", "ward-3", "Broken collection bin at bus stop",    ComplaintCategory.BROKEN_BIN,       ComplaintStatus.ASSIGNED,    Priority.MEDIUM,   now - timedelta(days=4),  9.9330, 78.2250),
            ("comp-004", "user-citizen2", "ward-4", "Street waste scattered after rain",    ComplaintCategory.STREET_WASTE,     ComplaintStatus.NEW,         Priority.LOW,      now - timedelta(days=3),  9.9295, 78.2160),
            ("comp-005", "user-citizen3", "ward-5", "Drain blockage causing water logging", ComplaintCategory.DRAIN_BLOCKAGE,   ComplaintStatus.VERIFICATION,Priority.HIGH,     now - timedelta(days=2),  9.9310, 78.2220),
            ("comp-006", "user-citizen3", "ward-1", "Burning garbage near school",          ComplaintCategory.GARBAGE_OVERFLOW, ComplaintStatus.ESCALATED,   Priority.CRITICAL, now - timedelta(days=6),  9.9320, 78.2200),
            ("comp-007", "user-citizen1", "ward-2", "Old sofa abandoned on footpath",       ComplaintCategory.ILLEGAL_DUMPING,  ComplaintStatus.NEW,         Priority.MEDIUM,   now - timedelta(days=1),  9.9285, 78.2215),
            ("comp-008", "user-citizen2", "ward-3", "Rubbish near temple entrance",         ComplaintCategory.STREET_WASTE,     ComplaintStatus.RESOLVED,    Priority.HIGH,     now - timedelta(days=10), 9.9340, 78.2255),
            ("comp-009", "user-citizen3", "ward-4", "Overflowing bin at park entrance",     ComplaintCategory.GARBAGE_OVERFLOW, ComplaintStatus.NEW,         Priority.MEDIUM,   now - timedelta(hours=6), 9.9290, 78.2170),
            ("comp-010", "user-citizen1", "ward-5", "Dead animal near drain",               ComplaintCategory.OTHER,            ComplaintStatus.ASSIGNED,    Priority.HIGH,     now - timedelta(hours=3), 9.9315, 78.2225),
        ]

        def ref(n): 
            return f"KLD-{now.strftime('%y%m')}-{n:04X}"

        for i, (cid, uid, wid, title, cat, status, pri, created, lat, lng) in enumerate(complaints_data):
            resolved_at = created + timedelta(days=2) if status == ComplaintStatus.RESOLVED else None
            db.add(Complaint(
                id=cid, reference_number=ref(i+1),
                user_id=uid, ward_id=wid, title=title,
                description=f"Detailed report: {title}. Immediate attention required.",
                category=cat, status=status, priority=pri,
                latitude=lat, longitude=lng,
                address=f"Near main road, {wid.replace('-', ' ').title()}",
                created_at=created, updated_at=created,
                resolved_at=resolved_at
            ))
        db.commit()

        # --- Tasks ---
        print("Seeding tasks...")
        tasks = [
            Task(id="task-001", complaint_id="comp-001", worker_id="user-worker1", assigned_by="user-je1", status=TaskStatus.COMPLETED, priority=Priority.HIGH,     notes="Clear overflowing bin",         started_at=now-timedelta(days=6), completed_at=now-timedelta(days=5)),
            Task(id="task-002", complaint_id="comp-002", worker_id="user-worker1", assigned_by="user-je1", status=TaskStatus.STARTED,   priority=Priority.CRITICAL, notes="Remove illegal dumping urgently", started_at=now-timedelta(days=4)),
            Task(id="task-003", complaint_id="comp-003", worker_id="user-worker2", assigned_by="user-sup1", status=TaskStatus.ASSIGNED,  priority=Priority.MEDIUM,   notes="Replace broken bin at bus stop"),
            Task(id="task-004", complaint_id="comp-005", worker_id="user-worker2", assigned_by="user-sup1", status=TaskStatus.VERIFICATION, priority=Priority.HIGH,  notes="Clear drain blockage",            started_at=now-timedelta(days=1)),
            Task(id="task-005", complaint_id="comp-008", worker_id="user-worker1", assigned_by="user-je1", status=TaskStatus.COMPLETED, priority=Priority.HIGH,     notes="Clean temple area",               started_at=now-timedelta(days=9), completed_at=now-timedelta(days=8)),
        ]
        db.add_all(tasks)
        db.commit()

        # --- Verifications ---
        print("Seeding verifications...")
        verifications = [
            Verification(
                id="verif-001", task_id="task-001",
                before_image_url="https://placehold.co/400x300/1a2a3a/white?text=Before+-+Bin+Overflow",
                before_lat=9.9312, before_lng=78.2196,
                before_captured_at=now - timedelta(days=6),
                after_image_url="https://placehold.co/400x300/1a3a2a/white?text=After+-+Bin+Cleared",
                after_lat=9.9312, after_lng=78.2196,
                after_captured_at=now - timedelta(days=5),
                distance_from_complaint=12.5, location_verified=True,
                approval_status="APPROVED", approved_by="user-sup1",
                approval_remarks="Good work, area fully cleaned.",
                approved_at=now - timedelta(days=5)
            ),
            Verification(
                id="verif-002", task_id="task-004",
                before_image_url="https://placehold.co/400x300/3a1a1a/white?text=Before+-+Drain+Block",
                before_lat=9.9310, before_lng=78.2220,
                before_captured_at=now - timedelta(days=1),
                after_image_url="https://placehold.co/400x300/1a3a2a/white?text=After+-+Drain+Clear",
                after_lat=9.9310, after_lng=78.2220,
                after_captured_at=now - timedelta(hours=4),
                distance_from_complaint=8.2, location_verified=True,
                approval_status="PENDING",
            ),
            Verification(
                id="verif-003", task_id="task-005",
                before_image_url="https://placehold.co/400x300/1a2a3a/white?text=Before+-+Temple+Area",
                before_lat=9.9340, before_lng=78.2255,
                before_captured_at=now - timedelta(days=9),
                after_image_url="https://placehold.co/400x300/1a3a2a/white?text=After+-+Temple+Clean",
                after_lat=9.9340, after_lng=78.2255,
                after_captured_at=now - timedelta(days=8),
                distance_from_complaint=5.0, location_verified=True,
                approval_status="APPROVED", approved_by="user-sup1",
                approval_remarks="Area cleaned properly.",
                approved_at=now - timedelta(days=8)
            ),
        ]
        db.add_all(verifications)
        db.commit()

        print("\nDatabase seeded successfully!")
        print("=" * 50)
        print("  Users created:")
        print("    admin@keeladi.gov          -> ADMIN")
        print("    je.kumar@keeladi.gov       -> JUNIOR_ENGINEER")
        print("    supervisor@keeladi.gov     -> SUPERVISOR")
        print("    driver1@keeladi.gov        -> DRIVER")
        print("    driver2@keeladi.gov        -> DRIVER")
        print("    sanitation.worker@...      -> SANITATION_WORKER")
        print("    worker2@keeladi.gov        -> SANITATION_WORKER")
        print("    john.doe@keeladi.gov       -> CITIZEN")
        print("    priya.s@keeladi.gov        -> CITIZEN")
        print("    raman.m@keeladi.gov        -> CITIZEN")
        print("  All passwords: password")
        print("=" * 50)
        print(f"  5 wards | 6 vehicles | 10 complaints | 5 tasks | 3 verifications")

    except Exception as e:
        import traceback
        print(f"ERROR seeding database: {e}")
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
