from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # API Config
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Web3
    RPC_URL: str = "http://localhost:8545"
    PRIVATE_KEY: str = ""
    CONTRACT_ADDRESS: str = ""

    # Noir
    NOIR_CIRCUIT_PATH: str = "/app/circuits/gym_verify"

    # Mock data (substituir por DB)
    GYM_LAT: str = "37423642"
    GYM_LONG: str = "57915942"

    class Config:
        env_file = ".env"


settings = Settings()
