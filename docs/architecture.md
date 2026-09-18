# Architecture

Client -> FastAPI Routes -> Services/Repositories -> SQLAlchemy ORM -> MySQL

Authentication uses JWT access/refresh tokens.
Argon2 is used for password hashing.
Business rules are enforced at API/service/database levels.
