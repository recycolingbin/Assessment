from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import engine, Base
from app.routers import auth_router, assets_router, transactions_router, portfolio_router
import traceback

app = FastAPI(
    title="Portfolio Management API",
    description="API for managing investment portfolio",
    version="1.0.0"
)

# CORS middleware - MUST be added before other middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler to ensure CORS headers are included in error responses
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the full exception
    print(f"\nException occurred: {str(exc)}")
    traceback.print_exc()
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
    )

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)
app.include_router(assets_router)
app.include_router(transactions_router)
app.include_router(portfolio_router)

@app.get("/")
def root():
    return {"message": "Portfolio Management API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
