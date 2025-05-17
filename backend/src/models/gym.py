from pydantic import BaseModel, Field
from typing import Optional


class GymBase(BaseModel):
    name: str
    lat: float = Field(..., description="Latitude multiplicada por 10^6")
    long: float = Field(..., description="Longitude multiplicada por 10^6")
    max_distance: int = Field(..., description="Distância máxima em metros")


class GymCreate(GymBase):
    pass


class Gym(GymBase):
    id: int
    active: bool = True


class ProofRequest(BaseModel):
    user_lat: float
    user_long: float
    gym_id: int
