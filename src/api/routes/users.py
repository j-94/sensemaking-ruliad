#!/usr/bin/env python3
"""
User management API routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ...core.database import get_db
from ...services.user_service import UserService
from ...core.engine import ConsciousnessEngine

router = APIRouter()


@router.post("/onboard", summary="Onboard Random User", description="Create a random user with consciousness profiling (preserved feature)")
async def onboard_user(db: Session = Depends(get_db)):
    """Onboard a random user with AI agent assignment (preserved from original)"""
    try:
        engine = ConsciousnessEngine()  # Would be injected in real implementation
        user_service = UserService(db, engine)

        result = user_service.create_random_user()

        return {
            "user": result["user"],
            "agent": result["agent"],
            "message": "User onboarded with consciousness-powered agent"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Onboarding failed: {str(e)}")


@router.get("/", summary="List Users", description="Get paginated list of users")
async def get_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get paginated list of users"""
    try:
        engine = ConsciousnessEngine()
        user_service = UserService(db, engine)

        result = user_service.get_users(page=page, limit=limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve users: {str(e)}")


@router.get("/profile", summary="User Profile", description="Get current user profile")
async def get_user_profile(db: Session = Depends(get_db)):
    """Get current user profile (requires authentication)"""
    # In real implementation, this would get user from JWT token
    # For now, return a mock response
    return {
        "id": "current-user-id",
        "name": "Current User",
        "email": "user@example.com",
        "role": "Developer",
        "intelligence_level": 85,
        "onboarded_at": "2024-01-01T00:00:00Z"
    }


@router.get("/statistics", summary="User Statistics", description="Get comprehensive user statistics")
async def get_user_statistics(db: Session = Depends(get_db)):
    """Get comprehensive user statistics"""
    try:
        engine = ConsciousnessEngine()
        user_service = UserService(db, engine)

        stats = user_service.get_user_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")


@router.get("/{user_id}", summary="Get User", description="Get detailed user information")
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get detailed user information by ID"""
    try:
        engine = ConsciousnessEngine()
        user_service = UserService(db, engine)

        user = user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user: {str(e)}")