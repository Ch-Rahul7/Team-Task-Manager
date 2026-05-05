# Railway-safe minimal api.py
from fastapi import FastAPI

app = FastAPI(title="Team Task Manager - Reset")

@app.get("/")
async def root():  # ← async def fixed!
    return {"message": "Backend ALIVE on Railway!", "status": "healthy"}

@app.on_event("startup")
async def startup():  # ← async def fixed!
    print("🚀 Railway backend starting - Reset mode")
    print("✅ Root endpoint working!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)