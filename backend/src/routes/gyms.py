from fastapi import APIRouter, HTTPException
from typing import List
from ..models.gym import Gym

router = APIRouter()

# Mock de academias para o MVP
gyms = {
    1: Gym(
        id=1,
        name="Academia Central",
        lat=37.423642,
        long=-122.084058,
        max_distance=100,
    ),
    2: Gym(
        id=2,
        name="Fitness Plus",
        lat=37.422081,
        long=-122.084438,
        max_distance=150,
    ),
}


@router.get("/gyms", response_model=List[Gym])
async def list_gyms():
    """Lista todas as academias disponíveis"""
    return list(gyms.values())


@router.get("/gym/{gym_id}", response_model=Gym)
async def get_gym(gym_id: int):
    """Retorna detalhes de uma academia específica"""
    if gym_id not in gyms:
        raise HTTPException(status_code=404, detail="Academia não encontrada")
    return gyms[gym_id]
