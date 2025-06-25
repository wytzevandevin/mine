from fastapi import APIRouter

from app.api.v1.endpoints import auth, truck, digger, dump, assign, dashboard
from app.config import get_settings

settings = get_settings()

api_router = APIRouter(prefix=settings.API_V1_STR)

# Include auth router
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include auth router
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

# Include truck router
api_router.include_router(truck.router, prefix="/trucks", tags=["trucks"])

# Include diggers router
api_router.include_router(digger.router, prefix="/diggers", tags=["diggers"])

# Include dumps router
api_router.include_router(dump.router, prefix="/dumps", tags=["dumps"])

# Include assign router
api_router.include_router(assign.router, prefix="/assignments", tags=["assignments"])

# Import and include other routers here
# Example:
# from .endpoints import users, items
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(items.router, prefix="/items", tags=["items"]) 