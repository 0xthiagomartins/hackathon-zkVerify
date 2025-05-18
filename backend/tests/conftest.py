import sys
import os
from pathlib import Path
import pytest
import requests
import time
from fastapi.testclient import TestClient
from src.main import app

# Adicionar o diretório raiz do projeto ao PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))


@pytest.fixture(scope="session", autouse=True)
def ensure_api_running():
    """Garantir que a API está rodando antes de executar os testes"""
    client = TestClient(app)
    max_retries = 5
    retry_delay = 1

    for i in range(max_retries):
        try:
            response = client.get("/health")
            if response.status_code == 200:
                return
        except:
            if i < max_retries - 1:
                time.sleep(retry_delay)
                continue
            raise Exception("API não está respondendo")
