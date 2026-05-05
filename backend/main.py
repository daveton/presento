import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.generate import router as generate_router
from api.templates import router as templates_router

app = FastAPI(title="Presento API", version="0.1.0")

# CORS - 支持多种部署环境
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5666",
    "http://localhost:5668",
    "http://192.168.10.105:5668",
]
if os.getenv("ALLOWED_ORIGINS"):
    allowed_origins.extend(os.getenv("ALLOWED_ORIGINS").split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(generate_router, prefix="/api")
app.include_router(templates_router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3301)
