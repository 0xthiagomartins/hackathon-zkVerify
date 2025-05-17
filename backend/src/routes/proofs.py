from fastapi import APIRouter, HTTPException
from ..models.gym import ProofRequest

router = APIRouter()


@router.post("/generate-proof")
async def generate_proof(request: ProofRequest):
    """Gera uma prova ZK para check-in em uma academia"""
    try:
        # Mock da resposta por enquanto
        return {
            "proof": "0x...",
            "public_inputs": ["0", "0", "0", "0"],
            "success": True,
            "message": "Prova gerada com sucesso",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
