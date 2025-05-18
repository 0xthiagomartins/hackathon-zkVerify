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
    user_lat: int  # Multiplicado por 10^6
    user_long: int  # Multiplicado por 10^6
    gym_id: int

    class Config:
        json_schema_extra = {
            "example": {"user_lat": 37423640, "user_long": -122084050, "gym_id": 1}
        }
