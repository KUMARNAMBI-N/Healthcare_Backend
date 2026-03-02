# Healthcare SaaS Project

This is a real-time Healthcare SaaS project built with FastAPI, PostgreSQL, Redis, and Kafka.

## Prerequisites
- Python 3.10+
- PostgreSQL (or run via Docker)
- Redis (or run via Docker)
- Kafka (or run via Docker)

## Setup Instructions

### 1. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage your dependencies.
```bash
python -m venv venv
```

### 2. Activate the Virtual Environment
- **Windows:**
  ```bash
  .\venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
Ensure you have a PostgreSQL database running and update the `DATABASE_URL` in `app/config.py` (or your `.env` file) to match your credentials.

## Running the Application

To run the FastAPI server locally with live-reloading:

```bash
uvicorn app.main:app --reload
```

The API will be available at: http://127.0.0.1:8000
Interactive API Documentation (Swagger UI): http://127.0.0.1:8000/docs
Alternative API Documentation (ReDoc): http://127.0.0.1:8000/redoc
