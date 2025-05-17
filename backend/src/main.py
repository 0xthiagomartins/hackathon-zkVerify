from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .routes import gyms, proofs

app = FastAPI(
    title="DeGym zkVerify API",
    description="API para verificação de presença em academias usando ZK Proofs",
    version="0.1.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas
app.include_router(gyms, tags=["gyms"])
app.include_router(proofs, tags=["proofs"])


@app.get("/health")
async def health_check():
    """Endpoint para verificar a saúde da API"""
    return {"status": "healthy"}
