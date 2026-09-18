from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str = Field(min_length=8)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: Optional[str]
    role: str
    is_active: bool
    model_config = {"from_attributes": True}

class EventCreate(BaseModel):
    event_name: str
    description: Optional[str] = None
    event_type: str
    start_date: datetime
    end_date: datetime
    registration_start: datetime
    registration_end: datetime
    capacity: int = Field(gt=0)
    city: Optional[str] = None
    venue_id: Optional[int] = None
    status: str = "Draft"

class VenueCreate(BaseModel):
    venue_name: str
    address: str
    city: str
    capacity: int = Field(gt=0)
    facilities: Optional[str] = None
    status: str = "Active"

class HallCreate(BaseModel):
    hall_name: str
    capacity: int = Field(gt=0)
    floor: Optional[int] = None
    availability_status: str = "Available"

class SpeakerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    bio: Optional[str] = None
    expertise: Optional[str] = None
    company: Optional[str] = None
    experience: int = 0

class SessionCreate(BaseModel):
    event_id: int
    speaker_id: Optional[int] = None
    hall_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    capacity: int = Field(gt=0)
    session_type: str

class TicketCreate(BaseModel):
    ticket_type: str
    price: float = Field(ge=0)
    quantity: int = Field(gt=0)
    sale_start: datetime
    sale_end: datetime

class PurchaseCreate(BaseModel):
    quantity: int = Field(gt=0)

class PaymentCreate(BaseModel):
    transaction_id: str
    payment_method: str
    amount: float = Field(ge=0)
    payment_status: str

class FeedbackCreate(BaseModel):
    registration_id: int
    event_id: int
    speaker_id: Optional[int] = None
    session_id: Optional[int] = None
    rating: int = Field(ge=1, le=5)
    feedback: Optional[str] = None
