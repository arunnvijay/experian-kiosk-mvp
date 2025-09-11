# Backend Authentication Module - Updated for Username-Only Auth
# File: backend/auth.py

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import json
import os
import re
from datetime import datetime, timedelta
from typing import Optional

# Initialize router
auth_router = APIRouter(prefix="/api/auth", tags=["authentication"])
security = HTTPBearer(auto_error=False)

# Data models
class LoginRequest(BaseModel):
    username: str  # Only username field now

class LoginResponse(BaseModel):
    success: bool
    message: str
    username: Optional[str] = None
    session_id: Optional[str] = None

class UserSession(BaseModel):
    username: str
    session_id: str
    created_at: datetime
    last_activity: datetime

# In-memory session storage (for MVP - replace with Redis/DB in production)
active_sessions = {}

def generate_session_id(username: str) -> str:
    """Generate a simple session ID for MVP"""
    from hashlib import md5
    import time
    return md5(f"{username}_{time.time()}".encode()).hexdigest()

def create_session(username: str) -> str:
    """Create a new user session"""
    session_id = generate_session_id(username)
    active_sessions[session_id] = {
        'username': username,
        'created_at': datetime.now(),
        'last_activity': datetime.now()
    }
    return session_id

def validate_session(session_id: str) -> Optional[str]:
    """Validate session and return username if valid"""
    if session_id in active_sessions:
        session = active_sessions[session_id]
        # Update last activity
        session['last_activity'] = datetime.now()
        return session['username']
    return None

def cleanup_expired_sessions():
    """Remove expired sessions (older than 8 hours)"""
    now = datetime.now()
    expired_sessions = []
    
    for session_id, session_data in active_sessions.items():
        if now - session_data['last_activity'] > timedelta(hours=8):
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        del active_sessions[session_id]

def is_valid_username(username: str) -> bool:
    """Validate username format"""
    if not username or len(username.strip()) < 2:
        return False
    
    username = username.strip()
    
    # Basic validation rules
    if len(username) < 2 or len(username) > 50:
        return False
    
    # Allow letters, spaces, dots, hyphens, and apostrophes
    if not re.match(r"^[a-zA-Z\s.'-]+$", username):
        return False
    
    return True

@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Authenticate user with username only (simplified MVP version)
    """
    try:
        print(f"Login attempt for username: {request.username}")
        
        # Clean up expired sessions
        cleanup_expired_sessions()
        
        # Validate username format
        if not is_valid_username(request.username):
            return LoginResponse(
                success=False,
                message="Please enter a valid name (2-50 characters, letters only)"
            )
        
        # Clean username
        clean_username = request.username.strip()
        
        # Create session for valid username
        session_id = create_session(clean_username)
        
        print(f"Login successful for: {clean_username}")
        
        return LoginResponse(
            success=True,
            message="Access granted",
            username=clean_username,
            session_id=session_id
        )
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Logout user and invalidate session
    """
    try:
        if credentials:
            session_id = credentials.credentials
            if session_id in active_sessions:
                username = active_sessions[session_id]['username']
                del active_sessions[session_id]
                print(f"Logout successful for: {username}")
                return {"success": True, "message": "Logged out successfully"}
        
        return {"success": True, "message": "Session not found or already expired"}
        
    except Exception as e:
        print(f"Logout error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.get("/validate")
async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Validate session token and return user info
    """
    try:
        if not credentials:
            raise HTTPException(status_code=401, detail="No session token provided")
        
        session_id = credentials.credentials
        username = validate_session(session_id)
        
        if username:
            return {
                "valid": True,
                "username": username,
                "session_id": session_id
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid or expired session")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Token validation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.get("/status")
async def auth_status():
    """
    Get authentication system status (for debugging)
    """
    try:
        cleanup_expired_sessions()
        
        # Get session statistics
        total_sessions = len(active_sessions)
        recent_sessions = sum(1 for session in active_sessions.values() 
                            if datetime.now() - session['last_activity'] < timedelta(hours=1))
        
        return {
            "authentication_type": "username_only",
            "active_sessions": total_sessions,
            "recent_sessions": recent_sessions,
            "system_status": "operational"
        }
    except Exception as e:
        print(f"Status check error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.get("/sessions")
async def get_active_sessions():
    """
    Get list of active sessions (for admin/debugging)
    """
    try:
        cleanup_expired_sessions()
        
        sessions = []
        for session_id, session_data in active_sessions.items():
            sessions.append({
                "session_id": session_id[:8] + "...",  # Truncated for security
                "username": session_data['username'],
                "created_at": session_data['created_at'].isoformat(),
                "last_activity": session_data['last_activity'].isoformat(),
                "duration_minutes": int((datetime.now() - session_data['created_at']).total_seconds() / 60)
            })
        
        return {
            "active_sessions": sessions,
            "total_count": len(sessions)
        }
        
    except Exception as e:
        print(f"Sessions list error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Dependency for protected routes
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to get current authenticated user
    Use this in other routes that require authentication
    """
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    session_id = credentials.credentials
    username = validate_session(session_id)
    
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    return username

# Helper function for username validation (can be used by other modules)
def validate_username_format(username: str) -> tuple[bool, str]:
    """
    Validate username and return (is_valid, error_message)
    """
    if not username:
        return False, "Username is required"
    
    username = username.strip()
    
    if len(username) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(username) > 50:
        return False, "Name must be less than 50 characters"
    
    if not re.match(r"^[a-zA-Z\s.'-]+$", username):
        return False, "Name can only contain letters, spaces, dots, hyphens, and apostrophes"
    
    return True, ""

# Test function to run this module directly (for debugging)
if __name__ == "__main__":
    print("Updated Auth module loaded successfully!")
    print("Authentication type: Username only")
    
    # Test username validation
    test_names = ["John Smith", "Admin", "Mary O'Connor", "Jean-Pierre", "A", "123Invalid", "Valid Name"]
    for name in test_names:
        is_valid, error = validate_username_format(name)
        print(f"'{name}': {'✓' if is_valid else '✗'} {error if not is_valid else ''}")