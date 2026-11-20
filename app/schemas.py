from datetime import date, time, timedelta
from typing import Literal

from pydantic import BaseModel, Field, field_validator

MAX_DAYS_AHEAD = 30
OPEN_HOUR, CLOSE_HOUR = 12, 22


class BookingCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    phone: str = Field(pattern=r"^\+7\d{10}$")
    booking_date: date
    booking_time: time
    guests: int = Field(ge=1, le=10)

    @field_validator("booking_date")
    @classmethod
    def date_in_range(cls, value: date) -> date:
        today = date.today()
        if not today <= value <= today + timedelta(days=MAX_DAYS_AHEAD):
            raise ValueError(f"Date must be within the next {MAX_DAYS_AHEAD} days")
        return value

    @field_validator("booking_time")
    @classmethod
    def whole_hour_in_range(cls, value: time) -> time:
        is_whole = value.minute == 0 and value.second == 0 and value.microsecond == 0
        if not is_whole or not OPEN_HOUR <= value.hour <= CLOSE_HOUR:
            raise ValueError(f"Time must be a whole hour from {OPEN_HOUR}:00 to {CLOSE_HOUR}:00")
        return value


class BookingOut(BaseModel):
    id: int
    name: str
    phone: str
    booking_date: date
    booking_time: time
    guests: int
    status: Literal["active", "cancelled"]
