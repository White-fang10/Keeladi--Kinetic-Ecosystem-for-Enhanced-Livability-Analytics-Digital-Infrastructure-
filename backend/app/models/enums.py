import enum


class UserRole(str, enum.Enum):
    """Simplified 3-role system. Citizens don't need accounts."""
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    WORKER = "WORKER"
    CITIZEN = "CITIZEN"


class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class ComplaintCategory(str, enum.Enum):
    GARBAGE_OVERFLOW = "GARBAGE_OVERFLOW"
    ILLEGAL_DUMPING = "ILLEGAL_DUMPING"
    BROKEN_BIN = "BROKEN_BIN"
    STREET_WASTE = "STREET_WASTE"
    DRAIN_BLOCKAGE = "DRAIN_BLOCKAGE"
    OTHER = "OTHER"


class ComplaintStatus(str, enum.Enum):
    NEW = "NEW"
    PROCESSING = "PROCESSING"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    VERIFICATION = "VERIFICATION"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"


class Priority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TaskStatus(str, enum.Enum):
    CREATED = "CREATED"
    ASSIGNED = "ASSIGNED"
    STARTED = "STARTED"
    VERIFICATION = "VERIFICATION"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REASSIGNED = "REASSIGNED"


class VehicleType(str, enum.Enum):
    COMPACTOR = "COMPACTOR"
    TIPPER = "TIPPER"
    AUTO_TIPPER = "AUTO_TIPPER"
    MINI_TRUCK = "MINI_TRUCK"


class VehicleStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    COLLECTING = "COLLECTING"
    FULL = "FULL"
    DISPOSAL = "DISPOSAL"
    MAINTENANCE = "MAINTENANCE"


class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
