from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, Base
from .api import (
    auth, items, messages, admin, anonymous,
    enhanced_items, enhanced_messages, enhanced_admin, payments, chat, manual_payments
)
from .api import manual_payment_fix
from sqlalchemy import text
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="IMIS API - Complete System",
    description="Ishakiro Information Management System - Complete Lost & Found Platform for Rwanda",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration - Allow production domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5178",
        "http://localhost:3000",
        "https://imis-frontend.pages.dev",
        "https://imis-backend.onrender.com",
        "https://imis-backend-wk7z.onrender.com",
        "https://ishakiro.ac.rw",
        "https://www.ishakiro.ac.rw",
        "https://e-shakiro.com",
        "https://www.e-shakiro.com"
    ],
    allow_origin_regex=r"https://.*\.pages\.dev",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    try:
        logger.info("Starting IMIS Backend...")
        from .models import enhanced_models
        
        # Test database connection first
        from .core.database import SessionLocal
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
            logger.info("Database connection successful")
        except Exception as db_error:
            logger.error(f"Database connection failed: {db_error}")
            raise db_error
        finally:
            db.close()
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully")
        
        # Log environment info
        database_url = os.getenv('DATABASE_URL', 'Not set')
        logger.info(f"Database URL configured: {'Yes' if database_url != 'Not set' else 'No'}")
        logger.info("IMIS Backend startup completed successfully")
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise e

# Include all routers
app.include_router(anonymous.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(manual_payments.router, prefix="/api")
app.include_router(manual_payment_fix.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(enhanced_items.router, prefix="/api")
app.include_router(enhanced_messages.router, prefix="/api")
app.include_router(payments.router, prefix="/api")
app.include_router(enhanced_admin.router, prefix="/api")
app.include_router(items.router, prefix="/legacy")
app.include_router(messages.router, prefix="/legacy")
app.include_router(admin.router, prefix="/legacy")

@app.get("/")
def root():
    return {"message": "IMIS API Running", "version": "3.0.0", "status": "healthy"}

@app.get("/health")
def health():
    """Health check endpoint"""
    try:
        # Test database connection
        from .core.database import SessionLocal
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "healthy", "database": "connected", "version": "3.0.0"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
