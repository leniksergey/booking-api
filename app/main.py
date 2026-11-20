from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routes import router
from app.service import BookingNotFoundError, SlotTakenError

app = FastAPI(title="Restaurant Booking API")
app.include_router(router)


@app.exception_handler(BookingNotFoundError)
def not_found_handler(request: Request, exc: BookingNotFoundError):
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.exception_handler(SlotTakenError)
def slot_taken_handler(request: Request, exc: SlotTakenError):
    return JSONResponse(status_code=409, content={"detail": exc.message})
