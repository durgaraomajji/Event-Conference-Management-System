from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.models import (
    user,
    event,
    venue,
    speaker,
    session,
    registration,
    ticket,
    purchase,
    payment,
)

from app.routes import (
    auth,
    events,
    venues,
    speakers,
    sessions,
    registrations,
    tickets,
    purchases,
    payments,
    checkin as checkin_routes,
    bookings,
    certificates,
    feedback as feedback_routes,
    dashboard,
    refunds,
    admin,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Event & Conference Management System",
    version="1.0.0",
    description="Advanced FastAPI Event and Conference Management API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(events.router, prefix=API_PREFIX)
app.include_router(venues.router, prefix=API_PREFIX)
app.include_router(speakers.router, prefix=API_PREFIX)
app.include_router(sessions.router, prefix=API_PREFIX)
app.include_router(registrations.router, prefix=API_PREFIX)
app.include_router(tickets.router, prefix=API_PREFIX)
app.include_router(purchases.router, prefix=API_PREFIX)
app.include_router(payments.router, prefix=API_PREFIX)
app.include_router(checkin_routes.router, prefix=API_PREFIX)
app.include_router(bookings.router, prefix=API_PREFIX)
app.include_router(certificates.router, prefix=API_PREFIX)
app.include_router(feedback_routes.router, prefix=API_PREFIX)
app.include_router(dashboard.router, prefix=API_PREFIX)
app.include_router(refunds.router, prefix=API_PREFIX)
app.include_router(admin.router, prefix=API_PREFIX)


@app.get("/")
def root():
    return {
        "message": "Event & Conference Management API is running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "MySQL",
        "driver": "PyMySQL",
    }