import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import video, analysis, coaching

def create_app() -> FastAPI:
    app = FastAPI(title="Slugger Sensei: Virtual Baseball Coach Backend")

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # Frontend origin
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
        allow_headers=["*"],  # Allow all headers
    )

    # Include API routers
    app.include_router(video.router, prefix="/video", tags=["video"])
    app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
    app.include_router(coaching.router, prefix="/coaching", tags=["coaching"])

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080)) 
    print(f"⚡ Starting FastAPI on PORT {port} ...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")