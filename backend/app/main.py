import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.services.inference_service import inference_service
from app.consumer import stream_consumer_service
from app.api.endpoints import alerts, metrics, traffic, health, models_info, mitigation
from app.api import ws

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ids_backend")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup:
    logger.info("Initializing Intrusion Detection System backend...")
    init_db()
    inference_service.load_models()

    if settings.AUTO_START_CONSUMER:
        logger.info("Starting background stream consumer...")
        await stream_consumer_service.start()

    yield

    # Shutdown:
    logger.info("Shutting down IDS backend...")
    await stream_consumer_service.stop()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Real-Time Network Threat Detection Platform with XGBoost, Isolation Forest & Event Streaming",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registrations
app.include_router(health.router)
app.include_router(ws.router)
app.include_router(alerts.router, prefix=settings.API_PREFIX)
app.include_router(metrics.router, prefix=settings.API_PREFIX)
app.include_router(traffic.router, prefix=settings.API_PREFIX)
app.include_router(models_info.router, prefix=settings.API_PREFIX)
app.include_router(mitigation.router, prefix=settings.API_PREFIX)

@app.get("/")
def root():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "active",
        "docs_url": "/docs"
    }
