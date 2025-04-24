import os
# Load environment variables *before* importing other project modules
from dotenv import load_dotenv
# Try loading .env from the current working directory or parent directories
load_dotenv() 

from fastapi import FastAPI

# Import API router *after* loading .env
from .api.v1.routes import router as api_v1_router

app = FastAPI(
    title="LangChain Agent API",
    description="API endpoint for a LangChain agent.",
    version="0.1.0",
)

# Include the API router
app.include_router(api_v1_router, prefix="/api/v1") # Using the imported router

# Placeholder root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the LangChain Agent API"}

# --- Run instruction (for local development) ---
# To run this app: uvicorn app.main:app --reload --app-dir .

if __name__ == "__main__":
    import uvicorn
    # Note: When running with uvicorn directly, it assumes the file is the entry point.
    # For the structure `agent_project/app/main.py`, you'd run from `agent_project`:
    # uvicorn app.main:app --reload
    # Specify the app object directly if running this file
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 