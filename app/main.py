from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.modules.identity.routes import auth_routes, user_routes

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to Healthcare SaaS API"}

# Example of router inclusion which will be uncomments as they are implemented
# app.include_router(auth_routes.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
# app.include_router(user_routes.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
# app.include_router(hospital_routes.router, prefix=f"{settings.API_V1_STR}/hospitals", tags=["hospitals"])
