# Complete Backend Application for Experian Kiosk MVP
# File: backend/app.py

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import authentication module
from auth import auth_router

# Create FastAPI application
app = FastAPI(
    title="Experian Kiosk MVP",
    description="Secure business knowledge and quiz system with username-only authentication",
    version="1.0.0"
)

# Configure CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication router
app.include_router(auth_router)

# Static file paths
frontend_dir = current_dir.parent / "frontend"
static_assets_dir = frontend_dir / "assets"
pages_dir = frontend_dir / "pages"

# Serve static assets (CSS, JS, images)
app.mount("/assets", StaticFiles(directory=str(static_assets_dir)), name="assets")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Experian Kiosk MVP",
        "version": "1.0.0",
        "authentication": "username_only"
    }

# API status endpoint
@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {
        "api": "running",
        "authentication": "username_only_enabled",
        "frontend": "connected",
        "features": ["quiz", "session_management", "user_tracking"]
    }

# Test endpoint for frontend integration
@app.get("/api/test")
async def test_endpoint():
    """Test endpoint to verify frontend-backend connection"""
    return {
        "message": "Backend is working!",
        "authentication_type": "username_only",
        "timestamp": "2024-01-15T10:30:00Z"
    }

# Serve HTML pages
@app.get("/")
async def serve_login():
    """Serve the login page"""
    login_file = pages_dir / "index.html"
    if login_file.exists():
        return FileResponse(str(login_file))
    else:
        raise HTTPException(status_code=404, detail="Login page not found")

@app.get("/index.html")
async def serve_login_alt():
    """Alternative route for login page"""
    return await serve_login()

@app.get("/dashboard.html")
async def serve_dashboard():
    """Serve the dashboard page"""
    dashboard_file = pages_dir / "dashboard.html"
    if dashboard_file.exists():
        return FileResponse(str(dashboard_file))
    else:
        raise HTTPException(status_code=404, detail="Dashboard page not found - create frontend/pages/dashboard.html")

@app.get("/quiz.html")
async def serve_quiz():
    """Serve the quiz page"""
    quiz_file = pages_dir / "quiz.html"
    if quiz_file.exists():
        return FileResponse(str(quiz_file))
    else:
        raise HTTPException(status_code=404, detail="Quiz page not found - create frontend/pages/quiz.html")

# Future API endpoints for when database team is ready
@app.get("/api/quiz/questions")
async def get_quiz_questions():
    """
    Get quiz questions (placeholder for database integration)
    """
    return {
        "message": "Quiz API not yet connected to database",
        "status": "coming_soon",
        "note": "Frontend uses mock data for now"
    }

@app.post("/api/quiz/submit")
async def submit_quiz_answer():
    """
    Submit quiz answer (placeholder for database integration)
    """
    return {
        "message": "Quiz submission API not yet connected to database",
        "status": "coming_soon",
        "note": "Frontend handles scoring locally for now"
    }

# 404 handler for other routes
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Redirect 404s to login page"""
    return FileResponse(str(pages_dir / "index.html"))

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 Starting Experian Kiosk MVP Server")
    print("=" * 60)
    print(f"📁 Frontend directory: {frontend_dir}")
    print(f"📄 Serving pages from: {pages_dir}")
    print(f"🎨 Static assets from: {static_assets_dir}")
    print("=" * 60)
    print("🌐 Server will be available at:")
    print("   • http://127.0.0.1:8000")
    print("   • http://localhost:8000")
    print("=" * 60)
    print("🔐 Authentication Type: USERNAME ONLY")
    print("   • No password required")
    print("   • Enter any valid name (2-50 characters)")
    print("   • Examples: Admin, John Smith, Demo User")
    print("=" * 60)
    print("📊 API Endpoints Available:")
    print("   • POST /api/auth/login - Username-only login")
    print("   • POST /api/auth/logout - Session logout")
    print("   • GET /api/auth/validate - Session validation")
    print("   • GET /api/auth/status - System status")
    print("   • GET /health - Health check")
    print("=" * 60)
    
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )