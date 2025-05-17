from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import subprocess
import json
import os
import logging
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO if not os.getenv("DEBUG") else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("degym-api")

app = FastAPI(
    title="DeGym zkVerify API",
    description="API para verificação de presença em academias usando ZK proofs",
    version="0.1.0",
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=json.loads(os.getenv("CORS_ORIGINS", '["http://localhost:3000"]')),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelos
class ProofRequest(BaseModel):
    user_lat: int  # Multiplicado por 10^6
    user_long: int  # Multiplicado por 10^6
    gym_id: int


class ProofResponse(BaseModel):
    proof: str
    public_inputs: List[str]
    success: bool
    message: str


# Mock de academias para o MVP
gyms = {
    1: {
        "id": 1,
        "name": "Academia Central",
        "lat": 37423642,
        "long": -122084058,
        "max_distance": 100,
    },
    2: {
        "id": 2,
        "name": "Fitness Plus",
        "lat": 37422081,
        "long": -122084438,
        "max_distance": 150,
    },
}


@app.get("/")
async def root():
    """Endpoint raiz para verificar se a API está online"""
    return {"status": "online", "version": "0.1.0"}


@app.get("/gyms")
async def get_gyms():
    """Retorna lista de todas as academias disponíveis"""
    return list(gyms.values())


@app.get("/gym/{gym_id}")
async def get_gym(gym_id: int):
    """Retorna detalhes de uma academia específica"""
    if gym_id not in gyms:
        raise HTTPException(status_code=404, detail="Academia não encontrada")
    return gyms[gym_id]


@app.post("/generate-proof")
async def generate_proof(request: ProofRequest) -> ProofResponse:
    """Gera uma prova ZK para check-in em uma academia"""
    try:
        if request.gym_id not in gyms:
            raise HTTPException(status_code=404, detail="Academia não encontrada")

        gym = gyms[request.gym_id]

        # Gerar prova usando o circuito Noir
        # TODO: Implementar chamada ao circuito Noir

        # Mock da resposta por enquanto
        return ProofResponse(
            proof="0x...",
            public_inputs=["0", "0", "0", "0"],
            success=True,
            message="Prova gerada com sucesso",
        )

    except Exception as e:
        logger.error(f"Erro ao gerar prova: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Endpoint para verificar a saúde da API"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
