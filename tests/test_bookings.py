from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routes import get_service
from app.service import BookingService


@pytest.fixture
def client():
    service = BookingService()
    app.dependency_overrides[get_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


def payload(**changes):
    data = {
        "name": "Иван",
        "phone": "+79991234567",
        "booking_date": (date.today() + timedelta(days=1)).isoformat(),
        "booking_time": "18:00",
        "guests": 2,
    }
    return data | changes


def test_create_booking(client):
    r = client.post("/bookings", json=payload())
    assert r.status_code == 201
    assert r.json()["status"] == "active"


def test_double_booking_returns_409(client):
    client.post("/bookings", json=payload())
    r = client.post("/bookings", json=payload(name="Пётр"))
    assert r.status_code == 409
    assert r.json() == {"detail": "Slot is already booked"}


def test_cancelled_slot_can_be_rebooked(client):
    first = client.post("/bookings", json=payload()).json()
    r = client.delete(f"/bookings/{first['id']}")
    assert r.status_code == 200 and r.json()["status"] == "cancelled"
    assert client.post("/bookings", json=payload()).status_code == 201


@pytest.mark.parametrize(
    "changes",
    [
        {"booking_date": (date.today() - timedelta(days=1)).isoformat()},
        {"booking_date": (date.today() + timedelta(days=31)).isoformat()},
        {"booking_time": "18:30"},
        {"booking_time": "11:00"},
        {"booking_time": "23:00"},
        {"phone": "89991234567"},
        {"guests": 11},
    ],
)
def test_invalid_data_returns_422(client, changes):
    assert client.post("/bookings", json=payload(**changes)).status_code == 422


def test_not_found_and_date_filter(client):
    assert client.get("/bookings/999").json() == {"detail": "Booking not found"}
    client.post("/bookings", json=payload())
    other = (date.today() + timedelta(days=2)).isoformat()
    assert len(client.get("/bookings", params={"date": other}).json()) == 0
    assert len(client.get("/bookings").json()) == 1
