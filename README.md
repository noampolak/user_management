# User Management System

A robust user management system built with FastAPI, featuring secure JWT authentication, PostgreSQL database integration, and Docker containerization.

## Features

- User registration and authentication
- JWT token-based security
- Password hashing with bcrypt
- User profile management
- PostgreSQL database with UUID primary keys
- Swagger UI documentation
- Docker containerization
- Alembic migrations

## Prerequisites

- Docker and Docker Compose
- Git

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/noampolak/user-management-system.git
cd user-management
```

2. Start the application using Docker Compose:

```bash
docker-compose up -d
```

This will start three containers:
- PostgreSQL database (port 5432)
- FastAPI application (port 8000)
- Alembic migrations 


The API will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

## API Endpoints

### Public Endpoints

- `POST /register` - Register a new user
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }
  ```

- `POST /login` - Login and receive JWT token
  ```json
  {
    "email": "john@example.com",
    "password": "SecurePass123"
  }
  ```

### Protected Endpoints (Requires JWT Token)

- `GET /profile` - Get current user profile
- `PATCH /update` - Update user information
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "password": "NewPass123",
    "disabled": false
  }
  ```
- `GET /users` - List all users (admin only and only for testing- TODO: remove)

## Authentication

The API uses JWT Bearer tokens for authentication. To access protected endpoints:

1. Login to receive a token
2. Include the token in the Authorization header:
   ```
   Authorization: Bearer <your_token>
   ```

## Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one digit


## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

## Security Features

- Password hashing using bcrypt
- JWT token authentication
- Email validation
- UUID primary keys
- Input validation using Pydantic models

