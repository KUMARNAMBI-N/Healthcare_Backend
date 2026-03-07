# Healthcare Platform Microservices

This is a real-time Healthcare SaaS project restructured into a microservices architecture using FastAPI, PostgreSQL, Redis, and Kafka.

## Prerequisites
- Python 3.10+
- Docker and Docker Compose (highly recommended for running infrastructure)

## Architecture Overview
The platform consists of several independent microservices behind an API gateway:
- `identity-service`: Handles auth, users, and RBAC
- `hospital-service`: Manages hospital profiles
- `doctor-service`: Manages doctor profiles
- `scheduling-service`: Availability templates and slots
- `booking-service`: Appointment booking logic
- `review-service`: Patient reviews
- `payment-service`: Razorpay integration
- `notification-service`: Email and event consumers

## Running the Project Locally

Because this is a microservices architecture, you must run each service independently if running them natively via Python.

### 1. Set up Virtual Environment (Global or per-service)
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies
You should install the dependencies for each service. Currently, they share the base `requirements.txt` from the old monolith.
```bash
pip install -r services/identity-service/requirements.txt
```

### 3. Run a Specific Microservice (e.g. Identity Service)
Navigate to the root of the project. Tell `uvicorn` to look for the `main` app inside the service's `app` folder:
```bash
uvicorn services.identity-service.app.main:app --reload --port 8001
```

*Note: You will need to run each service on a different port (e.g., identity on 8001, booking on 8002).*

## Docker (Recommended - Pending Setup)
We have scaffolded `Dockerfile`s and a `docker-compose.yml` file in `infrastructure/`. Once this configuration is complete, running the entire stack will simply be:
```bash
docker-compose -f infrastructure/docker-compose.yml up --build
```
