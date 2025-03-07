from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import ai_doctor, auth, medicine, medical_conditions

app = FastAPI(
    title="AI Doctor API",
    description="API for AI Doctor consultations",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://symvii.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ai_doctor.router)
app.include_router(auth.router)
app.include_router(medicine.router)
app.include_router(medical_conditions.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 