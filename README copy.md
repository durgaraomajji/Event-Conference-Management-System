# Event & Conference Management System

FastAPI + SQLAlchemy + MySQL + PyMySQL + JWT + Argon2.

## MySQL

Create the database:

```sql
CREATE DATABASE event_management;
```

Open `app/config.py` and change:

```python
DATABASE_URL = "mysql+pymysql://root:YOUR_PASSWORD@127.0.0.1:3306/event_management"
```

## Windows PowerShell

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger:

`http://127.0.0.1:8000/docs`

## Demo order

1. Register attendee.
2. Create an Admin directly in the database or promote a registered user.
3. Login.
4. Authorize Swagger using Bearer token.
5. Create venue.
6. Create hall.
7. Create speaker.
8. Create event.
9. Create sessions.
10. Open registration.
11. Register attendee.
12. Create ticket.
13. Purchase ticket.
14. Process simulated successful payment.
15. Book session.
16. Check in using Staff/Admin.
17. Submit feedback.
18. Generate certificate.
19. Open admin dashboard.

Payment is simulated for local testing; no real money is processed.

## Alembic

After configuring MySQL:

```powershell
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

The application also creates missing tables automatically for easy local Swagger setup.
