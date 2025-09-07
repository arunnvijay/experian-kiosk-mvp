# Complete Backend Application for Experian Kiosk MVP
# File: backend/app.py

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from pathlib import Path

# Get current directory
current_dir = Path(__file__).parent

# Import authentication module (try-catch for development)
try:
    from auth import auth_router
except ImportError as e:
    print(f"Warning: Could not import auth module: {e}")
    print("Creating a basic auth router for testing...")
    
    # Create basic auth router for testing
    from fastapi import APIRouter
    auth_router = APIRouter(prefix="/api/auth", tags=["authentication"])
    
    @auth_router.post("/login")
    async def basic_login():
        return {"success": True, "message": "Basic login for testing"}

# Create FastAPI application
app = FastAPI(
    title="Experian Kiosk MVP",
    description="Secure business knowledge and quiz system",
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
        "version": "1.0.0"
    }

# API status endpoint
@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {
        "api": "running",
        "authentication": "enabled",
        "frontend": "connected"
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

# 404 handler for other routes
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return FileResponse(str(pages_dir / "index.html"))

if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("🚀 Starting Experian Kiosk MVP Server")
    print("=" * 50)
    print(f"📁 Frontend directory: {frontend_dir}")
    print(f"📄 Serving pages from: {pages_dir}")
    print(f"🎨 Static assets from: {static_assets_dir}")
    print("=" * 50)
    print("🌐 Server will be available at:")
    print("   • http://127.0.0.1:8000")
    print("   • http://localhost:8000")
    print("=" * 50)
    print("🔐 MVP Login Credentials:")
    print("   • Username: admin")
    print("   • Password: admin")
    print("=" * 50)
    
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )