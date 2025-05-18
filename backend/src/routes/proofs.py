from fastapi import APIRouter, HTTPException
from ..models.gym import ProofRequest
from ..core.config import settings
from web3 import Web3
import subprocess
import os
import json
from pathlib import Path

router = APIRouter()

# Cache simples em memória para provas
proof_cache = {}


def get_contract():
    # Carregar ABI do contrato
    contract_path = (
        Path(__file__).parent.parent.parent
        / "contracts/out/ZkCheckin.sol/ZkCheckin.json"
    )
    with open(contract_path) as f:
        contract_json = json.load(f)

    # Conectar ao nó RPC
    w3 = Web3(Web3.HTTPProvider(settings.RPC_URL))

    # Instanciar contrato
    contract = w3.eth.contract(
        address=settings.CONTRACT_ADDRESS, abi=contract_json["abi"]
    )

    return contract, w3


@router.post("/generate-proof")
async def generate_proof(request: ProofRequest):
    try:
        # Verificar cache
        cache_key = f"{request.user_lat}:{request.user_long}:{request.gym_id}"
        if cache_key in proof_cache:
            return proof_cache[cache_key]

        # Preparar inputs para o circuito
        with open(f"{settings.NOIR_CIRCUIT_PATH}/Prover.toml", "w") as f:
            f.write(
                f"""
                user_lat = "{request.user_lat}"
                user_long = "{request.user_long}"
                gym_lat = "{settings.GYM_LAT}"  # Mock - deveria vir do banco
                gym_long = "{settings.GYM_LONG}" # Mock - deveria vir do banco
                max_distance_squared = "1000000"  # 1km²
            """
            )

        # Gerar prova
        result = subprocess.run(
            ["nargo", "execute", "p"],
            cwd=settings.NOIR_CIRCUIT_PATH,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise Exception(f"Erro ao gerar prova: {result.stderr}")

        # Gerar prova com bb
        result = subprocess.run(
            [
                "bb",
                "prove",
                "-b",
                "./target/gym_verify.json",
                "-w",
                "./target/p.gz",
                "-o",
                "./target",
                "--oracle_hash",
                "keccak",
            ],
            cwd=settings.NOIR_CIRCUIT_PATH,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise Exception(f"Erro ao gerar prova bb: {result.stderr}")

        # Ler prova e inputs públicos
        with open(f"{settings.NOIR_CIRCUIT_PATH}/target/p.proof", "r") as f:
            proof = json.load(f)
        with open(f"{settings.NOIR_CIRCUIT_PATH}/target/p.public", "r") as f:
            public_inputs = json.load(f)

        response = {"success": True, "proof": proof, "public_inputs": public_inputs}

        # Guardar no cache
        proof_cache[cache_key] = response

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar prova: {str(e)}")
