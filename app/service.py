from datetime import date

from app.schemas import BookingCreate, BookingOut


class BookingNotFoundError(Exception):
    message = "Booking not found"


class SlotTakenError(Exception):
    message = "Slot is already booked"


class BookingService:
    def __init__(self) -> None:
        self._items: dict[int, BookingOut] = {}
        self._next_id = 1

    def create(self, data: BookingCreate) -> BookingOut:
        if self._slot_taken(data):
            raise SlotTakenError
        booking = BookingOut(id=self._next_id, status="active", **data.model_dump())
        self._items[booking.id] = booking
        self._next_id += 1
        return booking

    def list(self, on_date: date | None = None) -> list[BookingOut]:
        items = self._items.values()
        return [b for b in items if on_date is None or b.booking_date == on_date]

    def get(self, booking_id: int) -> BookingOut:
        try:
            return self._items[booking_id]
        except KeyError:
            raise BookingNotFoundError from None

    def cancel(self, booking_id: int) -> BookingOut:
        booking = self.get(booking_id)
        booking.status = "cancelled"
        return booking

    def _slot_taken(self, data: BookingCreate) -> bool:
        return any(
            b.status == "active"
            and b.booking_date == data.booking_date
            and b.booking_time == data.booking_time
            for b in self._items.values()
        )
