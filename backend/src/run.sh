#!/bin/bash
# Ativar ambiente virtual
source ../venv/bin/activate

# Executar a API
uvicorn main:app --host ${API_HOST:-0.0.0.0} --port ${API_PORT:-8000} --reload