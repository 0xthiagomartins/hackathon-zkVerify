# DeGym Backend

Backend para o projeto DeGym zkVerify, usando FastAPI e Noir para verificação de presença em academias.

## Estrutura do Projeto

```
backend/
├── api/
│   ├── core/          # Configurações e utilitários
│   ├── models/        # Modelos Pydantic
│   ├── routes/        # Rotas da API
│   └── services/      # Serviços (Noir, Web3)
├── tests/             # Testes
└── pyproject.toml     # Configuração do projeto
```

## Pré-requisitos

- Python 3.10+
- uv (gerenciador de pacotes Python)
- Nargo (Noir toolchain)

## Configuração do Ambiente

1. Instalar uv:
```bash
pip install uv
```

2. Criar e ativar ambiente virtual:
```bash
# Criar ambiente
uv venv

# Ativar (Linux/Mac)
source .venv/bin/activate
# ou (Windows)
.venv\Scripts\activate
```

3. Instalar dependências:
```bash
# Instalar dependências de desenvolvimento
uv pip install -e ".[dev]"
```

4. Criar arquivo .env:
```bash
cat > .env << EOL
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Web3
RPC_URL=http://localhost:8545
PRIVATE_KEY=your_private_key_here
CONTRACT_ADDRESS=your_contract_address_here

# Noir
NOIR_CIRCUIT_PATH=../circuits/gym_verify
EOL
```

## Executando a API

1. Método Direto:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

2. Usando o script:
```bash
chmod +x src/run.sh  # Apenas primeira vez (Linux/Mac)
./src/run.sh
```

A API estará disponível em: http://localhost:8000
Documentação Swagger: http://localhost:8000/docs

## Executando os Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=api

# Executar testes específicos
pytest tests/test_api.py -v
```

## Endpoints Disponíveis

- `GET /health` - Verificar status da API
- `GET /gyms` - Listar todas as academias
- `GET /gym/{gym_id}` - Obter detalhes de uma academia
- `POST /generate-proof` - Gerar prova ZK para check-in

## Desenvolvimento

1. Formatação do código:
```bash
# Formatar código
black api/ tests/

# Verificar estilo
ruff check api/ tests/
```

2. Verificar tipos:
```bash
mypy api/
```

## Troubleshooting

### Problemas Comuns

1. Erro de importação de módulos:
   - Verifique se está no diretório correto
   - Verifique se o ambiente virtual está ativado

2. Erro de conexão na API:
   - Verifique se as portas estão corretas no .env
   - Verifique se não há outro serviço usando a mesma porta

3. Erro nos testes:
   - Verifique se todas as dependências de desenvolvimento foram instaladas
   - Verifique se o arquivo .env está configurado corretamente 