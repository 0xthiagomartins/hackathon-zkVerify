# DeGym zkVerify - Backend

Este é o backend do projeto DeGym zkVerify, que consiste em uma API FastAPI e circuitos Noir para verificação de presença em academias.

## Estrutura do Projeto
```
backend/
├── api/                    # API FastAPI
│   ├── main.py            # Código principal da API
│   └── run.sh             # Script para executar a API
├── circuits/              # Circuitos Noir
│   └── gym_verify/        # Circuito de verificação de localização
│       └── src/
│           ├── main.nr    # Circuito principal
│           └── main.test.nr # Testes do circuito
└── tests/                 # Testes de integração
    └── integration_test.py
```

## Pré-requisitos

1. Python 3.10+
2. Nargo (Noir toolchain)
3. Ambiente virtual Python

## Configuração do Ambiente

### 1. Configurar ambiente Python
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Noir
```bash
# Verificar instalação do Nargo
nargo --version

# Se não estiver instalado, siga as instruções em:
# https://noir-lang.org/getting_started/nargo_installation
```

## Testando os Circuitos Noir

```bash
# Entrar no diretório do circuito
cd circuits/gym_verify  # Note o diretório correto

# Compilar o circuito
nargo check

# Executar testes
nargo test

# Para ver logs detalhados dos testes
nargo test -v
```

### Testando casos específicos
```bash
# Testar caso dentro do perímetro
nargo test test_within_range

# Testar caso fora do perímetro
nargo test test_outside_range
```

## Testando a API

### 1. Iniciar a API
```bash
# Entrar no diretório da API
cd api

# Dar permissão de execução ao script (Linux/Mac)
chmod +x run.sh

# Executar a API
./run.sh
# ou
bash run.sh
```

A API estará disponível em `http://localhost:8000`

### 2. Testar endpoints via Swagger UI
Acesse `http://localhost:8000/docs` para ver a documentação interativa e testar os endpoints.

### 3. Testar via cURL

```bash
# Verificar status da API
curl http://localhost:8000/health

# Listar academias
curl http://localhost:8000/gyms

# Obter detalhes de uma academia
curl http://localhost:8000/gym/1

# Gerar prova ZK (exemplo)
curl -X POST http://localhost:8000/generate-proof \
  -H "Content-Type: application/json" \
  -d '{
    "user_lat": 37423640,
    "user_long": -122084050,
    "gym_id": 1
  }'
```

### 4. Executar testes de integração
```bash
# No diretório raiz do backend
python -m pytest tests/integration_test.py -v
```

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# API Configuration
API_PORT=8000
API_HOST=0.0.0.0
DEBUG=true
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Blockchain
RPC_URL=http://localhost:8545
PRIVATE_KEY=your_private_key_here
CONTRACT_ADDRESS=your_contract_address_here
```

## Logs e Debugging

Os logs da API são salvos com diferentes níveis (INFO, DEBUG, ERROR) e podem ser visualizados no console.

Para habilitar logs mais detalhados:
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
```

## Troubleshooting

### Problemas comuns com o circuito Noir:
1. Erro de compilação: Verifique a sintaxe e tipos no arquivo `main.nr`
2. Falha nos testes: Verifique os valores de teste em `main.test.nr`

### Problemas comuns com a API:
1. Porta em uso: Mude a porta no arquivo `.env`
2. Erro CORS: Verifique a configuração de `CORS_ORIGINS`
3. Erro de conexão: Verifique se o ambiente virtual está ativado 