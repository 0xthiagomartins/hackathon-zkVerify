#!/bin/bash
# Ativar ambiente virtual
source ../../venv/bin/activate

# Executar a API
uvicorn main:app --host 0.0.0.0 --port 8000 --reload 