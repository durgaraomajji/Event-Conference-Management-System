from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SessionCreate(BaseModel):
    event_id: int
    speaker_id: int
    hall_id: int
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    capacity: int
    session_type: str


class SessionResponse(BaseModel):
    id: int
    event_id: int
    speaker_id: int
    hall_id: int
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    capacity: int
    session_type: str

    model_config = ConfigDict(from_attributes=True)