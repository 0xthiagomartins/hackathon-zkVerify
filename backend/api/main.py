from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import subprocess
import json
import os
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
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
    allow_origins=["*"],  # Ajustar para produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelos de dados
class Gym(BaseModel):
    id: int
    name: str
    lat: int  # Multiplicado por 10^6
    long: int  # Multiplicado por 10^6
    max_distance: int  # Em metros


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
    """Endpoint raiz para verificar se a API está funcionando"""
    return {"status": "online", "message": "DeGym zkVerify API"}


@app.get("/gyms", response_model=List[Dict[str, Any]])
async def get_gyms():
    """Retorna lista de academias disponíveis"""
    return list(gyms.values())


@app.get("/gym/{gym_id}", response_model=Dict[str, Any])
async def get_gym(gym_id: int):
    """Retorna informações da academia pelo ID"""
    if gym_id not in gyms:
        raise HTTPException(status_code=404, detail="Academia não encontrada")

    return gyms[gym_id]


@app.post("/generate-proof", response_model=ProofResponse)
async def generate_proof(request: ProofRequest):
    """Gera uma prova ZK para verificar a localização do usuário"""
    # Verificar se a academia existe
    if request.gym_id not in gyms:
        raise HTTPException(status_code=404, detail="Academia não encontrada")

    gym = gyms[request.gym_id]

    try:
        # Calcular o quadrado da distância máxima (para eficiência no cálculo)
        # Ajuste este cálculo conforme necessário para mapear corretamente unidades
        max_distance_squared = gym["max_distance"] * gym["max_distance"] * 10

        # Criar arquivo de input para o Nargo
        input_data = {
            "user_lat": str(request.user_lat),
            "user_long": str(request.user_long),
            "gym_lat": str(gym["lat"]),
            "gym_long": str(gym["long"]),
            "max_distance_squared": str(max_distance_squared),
        }

        # Caminho para o projeto Noir (ajuste conforme seu ambiente)
        noir_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "circuits", "gym_verify"
        )

        logger.info(f"Gerando prova com inputs: {input_data}")

        # Salvar os inputs em um arquivo
        with open(f"{noir_path}/Prover.toml", "w") as f:
            for key, value in input_data.items():
                f.write(f"{key} = {value}\n")

        # Executar Nargo para gerar a prova
        result = subprocess.run(
            ["nargo", "prove", "p"], cwd=noir_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            logger.error(f"Erro ao gerar prova: {result.stderr}")
            return ProofResponse(
                proof="",
                public_inputs=[],
                success=False,
                message=f"Erro ao gerar prova: {result.stderr}",
            )

        # Ler a prova gerada
        with open(f"{noir_path}/proofs/p.proof", "r") as f:
            proof = f.read().strip()

        # Ler os inputs públicos
        with open(f"{noir_path}/Verifier.toml", "r") as f:
            verifier_data = f.read()
            # Extrair os valores dos inputs públicos
            public_inputs = []
            for line in verifier_data.strip().split("\n"):
                if "=" in line:
                    value = line.split("=")[1].strip()
                    public_inputs.append(value)

        logger.info("Prova gerada com sucesso")

        return ProofResponse(
            proof=proof,
            public_inputs=public_inputs,
            success=True,
            message="Prova gerada com sucesso",
        )

    except Exception as e:
        logger.error(f"Erro ao gerar prova: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar prova: {str(e)}")


@app.get("/health")
async def health_check():
    """Endpoint para verificar a saúde da API"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
