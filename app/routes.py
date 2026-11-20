from datetime import date
from functools import lru_cache

from fastapi import APIRouter, Depends

from app.schemas import BookingCreate, BookingOut
from app.service import BookingService

router = APIRouter(prefix="/bookings", tags=["bookings"])


@lru_cache
def get_service() -> BookingService:
    return BookingService()


@router.post("", response_model=BookingOut, status_code=201)
def create_booking(data: BookingCreate, service: BookingService = Depends(get_service)):
    return service.create(data)


@router.get("", response_model=list[BookingOut])
def list_bookings(date: date | None = None, service: BookingService = Depends(get_service)):
    return service.list(date)


@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int, service: BookingService = Depends(get_service)):
    return service.get(booking_id)


@router.delete("/{booking_id}", response_model=BookingOut)
def cancel_booking(booking_id: int, service: BookingService = Depends(get_service)):
    return service.cancel(booking_id)
