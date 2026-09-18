from enum import Enum

class UserRole(str, Enum):
    ADMIN = "Admin"
    ORGANIZER = "Event Organizer"
    SPEAKER = "Speaker"
    STAFF = "Staff"
    ATTENDEE = "Attendee"

class EventType(str, Enum):
    CONFERENCE = "Conference"
    WORKSHOP = "Workshop"
    SEMINAR = "Seminar"
    MEETUP = "Meetup"
    TRAINING = "Training"

class EventStatus(str, Enum):
    DRAFT = "Draft"
    PUBLISHED = "Published"
    REGISTRATION_OPEN = "Registration Open"
    REGISTRATION_CLOSED = "Registration Closed"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class RegistrationStatus(str, Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    ATTENDED = "Attended"

class TicketType(str, Enum):
    STANDARD = "Standard"
    VIP = "VIP"
    EARLY_BIRD = "Early Bird"
    STUDENT = "Student"

class PaymentStatus(str, Enum):
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED = "Failed"
    REFUNDED = "Refunded"
