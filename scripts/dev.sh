#!/bin/bash

case "$1" in
  "up")
    docker-compose up -d
    echo "Aguardando API iniciar..."
    sleep 5
    curl http://localhost:8000/health || echo "API não está respondendo"
    ;;
  "down")
    docker-compose down
    ;;
  "build")
    docker-compose build
    ;;
  "logs")
    docker-compose logs -f
    ;;
  "status")
    echo "Status dos containers:"
    docker ps
    echo "\nLogs do backend:"
    docker logs hackathon-zkverify-backend-1
    ;;
  "noir-compile")
    docker-compose run --rm noir-builder bash -c "
      export PATH=/root/.cargo/bin:/root/.noir/bin:/root/.bb/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin && \
      source ~/.bashrc && \
      cd /app/circuits/gym_verify && \
      which nargo && \
      nargo --version && \
      nargo compile && \
      bb write_vk -b ./target/gym_verify.json -o ./target --oracle_hash keccak && \
      bb write_solidity_verifier -k ./target/vk -o ./target/Verifier.sol
    "
    ;;
  "noir-prove")
    docker-compose run --rm noir-builder bash -c "
      cd /app/circuits/gym_verify && \
      nargo execute p && \
      bb prove -b ./target/gym_verify.json -w ./target/p.gz -o ./target --oracle_hash keccak
    "
    ;;
  "test")
    docker-compose run --rm backend uv pip install -e ".[dev]" && pytest
    ;;
  "install")
    docker-compose run --rm backend uv pip install -e ".[dev]"
    ;;
  *)
    echo "Uso: ./dev.sh [comando]"
    echo "Comandos disponíveis:"
    echo "  up          - Inicia os containers"
    echo "  down        - Para os containers"
    echo "  build       - Rebuilda os containers"
    echo "  logs        - Mostra os logs"
    echo "  status      - Mostra status dos containers"
    echo "  noir-compile- Compila o circuito Noir"
    echo "  noir-prove  - Gera uma prova de teste"
    echo "  test        - Roda os testes"
    echo "  install     - Instala dependências usando uv"
    ;;
esac 

