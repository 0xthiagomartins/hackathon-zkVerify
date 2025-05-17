# Instruções para Desenvolvedor Backend - DeGym zkVerify MVP

## Visão Geral

Você está entrando no projeto DeGym, uma plataforma descentralizada para academias. Sua tarefa é desenvolver o **backend do MVP do componente zkVerify**, que permite verificar a presença dos usuários nas academias usando provas de conhecimento zero (para preservar privacidade).

**O objetivo simples**: Criar um sistema que gere provas ZK confirmando que usuários estão dentro do perímetro da academia, e smart contracts que verificam essas provas.

## Tecnologias que Você Vai Usar

- **Noir**: Linguagem para escrever circuitos de prova de conhecimento zero
- **Python** com **FastAPI**: Para API de backend
- **Foundry**: Para desenvolvimento dos smart contracts
- **OpenZeppelin**: Para contratos auxiliares

## Configuração do Ambiente (1-2 horas)

### Instalação do Noir
```bash
curl -L https://raw.githubusercontent.com/noir-lang/noirup/refs/heads/main/install | bash
noirup
```

### Configuração do Projeto Python
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install fastapi uvicorn pydantic web3
pip install pytest  # Para testes
```

### Configuração do Foundry
```bash
# Instalar Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Iniciar projeto
mkdir contracts
cd contracts
forge init
```

## O que Você Precisa Desenvolver (2-3 dias)

### 1. Circuito Noir (Prioridade Máxima - 1 dia)

Crie um diretório para o projeto Noir:
```bash
mkdir circuits
cd circuits
nargo init gym_verify
```

Implemente um circuito simples para verificar se o usuário está dentro do perímetro da academia (`src/main.nr`):

```rust
// Arquivo: src/main.nr
fn main(
    // Coordenadas do usuário (multiplicadas por 10^6 para precisão)
    user_lat: Field,
    user_long: Field,
    
    // Coordenadas da academia
    gym_lat: Field,
    gym_long: Field,
    
    // Distância máxima permitida (ao quadrado)
    max_distance_squared: Field
) {
    // Calcular diferença em coordenadas
    let lat_diff = if user_lat > gym_lat { 
        user_lat - gym_lat 
    } else { 
        gym_lat - user_lat 
    };
    
    let long_diff = if user_long > gym_long { 
        user_long - gym_long 
    } else { 
        gym_long - user_long 
    };
    
    // Versão simplificada do cálculo de distância (distância euclidiana ao quadrado)
    let distance_squared = lat_diff * lat_diff + long_diff * long_diff;
    
    // Verificar se o usuário está perto o suficiente
    constrain distance_squared <= max_distance_squared;
}
```

Compile e gere o verificador:
```bash
cd gym_verify
nargo compile
nargo codegen-verifier
```

### 2. API FastAPI (1 dia)

Crie um servidor básico com FastAPI (`main.py`):

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import subprocess
import json
import os

app = FastAPI(title="DeGym zkVerify API")

class ProofRequest(BaseModel):
    user_lat: int  # Multiplicado por 10^6
    user_long: int  # Multiplicado por 10^6
    gym_lat: int  # Multiplicado por 10^6
    gym_long: int  # Multiplicado por 10^6
    max_distance_squared: int

class ProofResponse(BaseModel):
    proof: str
    public_inputs: List[str]
    success: bool
    message: str

# Mock de academias para o MVP
gyms = {
    1: {"name": "Academia Central", "lat": 37423642, "long": -122084058, "max_distance": 100},
    2: {"name": "Fitness Plus", "lat": 37422081, "long": -122084438, "max_distance": 150},
}

@app.post("/generate-proof", response_model=ProofResponse)
async def generate_proof(request: ProofRequest):
    """Gera uma prova ZK para verificar a localização do usuário"""
    try:
        # Criar arquivo de input para o Nargo
        input_data = {
            "user_lat": str(request.user_lat),
            "user_long": str(request.user_long),
            "gym_lat": str(request.gym_lat),
            "gym_long": str(request.gym_long),
            "max_distance_squared": str(request.max_distance_squared)
        }
        
        # Caminho para o projeto Noir (ajuste conforme seu ambiente)
        noir_path = "noir-circuits/gym_verify"
        
        # Salvar os inputs em um arquivo
        with open(f"{noir_path}/Prover.toml", "w") as f:
            for key, value in input_data.items():
                f.write(f"{key} = {value}\n")
        
        # Executar Nargo para gerar a prova
        result = subprocess.run(
            ["nargo", "prove", "p"],
            cwd=noir_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return ProofResponse(
                proof="",
                public_inputs=[],
                success=False,
                message=f"Erro ao gerar prova: {result.stderr}"
            )
        
        # Ler a prova gerada
        with open(f"{noir_path}/proofs/p.proof", "r") as f:
            proof = f.read().strip()
        
        # Ler os inputs públicos
        with open(f"{noir_path}/Verifier.toml", "r") as f:
            verifier_data = f.read()
            # Extrair os valores dos inputs públicos
            public_inputs = []
            for line in verifier_data.strip().split("\n"):
                if "=" in line:
                    value = line.split("=")[1].strip()
                    public_inputs.append(value)
        
        return ProofResponse(
            proof=proof,
            public_inputs=public_inputs,
            success=True,
            message="Prova gerada com sucesso"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar prova: {str(e)}")

@app.get("/gyms")
async def get_gyms():
    """Retorna lista de academias disponíveis"""
    return list(gyms.values())

@app.get("/gym/{gym_id}")
async def get_gym(gym_id: int):
    """Retorna informações da academia pelo ID"""
    if gym_id not in gyms:
        raise HTTPException(status_code=404, detail="Academia não encontrada")
    
    return gyms[gym_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 3. Smart Contracts (1 dia)

Crie os contratos necessários usando Foundry:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

// Interface do verificador gerado pelo Noir
interface INoirVerifier {
    function verify(bytes calldata proof, uint256[] calldata publicInputs) external view returns (bool);
}

// Contrato simplificado para check-ins
contract ZkCheckin is Ownable {
    INoirVerifier public verifier;
    
    // Estrutura para armazenar informações das academias
    struct Gym {
        uint256 lat;  // Latitude * 10^6
        uint256 long; // Longitude * 10^6
        uint256 maxDistanceSquared;
        bool active;
    }
    
    // Mapeamento de academias registradas
    mapping(uint256 => Gym) public gyms;
    
    // Registrar check-ins (usuário => timestamp do último check-in)
    mapping(address => uint256) public lastCheckin;
    
    event CheckInCompleted(address user, uint256 gymId, uint256 timestamp);
    
    constructor(address _verifierAddress) Ownable(msg.sender) {
        verifier = INoirVerifier(_verifierAddress);
    }
    
    // Registrar uma nova academia
    function registerGym(
        uint256 gymId, 
        uint256 lat, 
        uint256 long, 
        uint256 maxDistanceMeters
    ) external onlyOwner {
        // Converter distância metros para unidades coordenadas ao quadrado (aproximação)
        uint256 maxDistanceSquared = maxDistanceMeters * maxDistanceMeters / 10;
        
        gyms[gymId] = Gym(lat, long, maxDistanceSquared, true);
    }
    
    // Fazer check-in com verificação ZK
    function checkin(
        uint256 gymId,
        bytes calldata zkProof,
        uint256[] calldata publicInputs
    ) external {
        // Verificar se a academia está registrada e ativa
        require(gyms[gymId].active, "Gym not active");
        
        // Verificar a prova ZK
        require(verifier.verify(zkProof, publicInputs), "Invalid ZK proof");
        
        // Registrar o check-in
        lastCheckin[msg.sender] = block.timestamp;
        
        // Emitir evento
        emit CheckInCompleted(msg.sender, gymId, block.timestamp);
    }
}
```

Compile os contratos:
```bash
cd contracts
forge build
```

## Como Testar

### Teste do Circuito Noir

Crie um arquivo de teste em `noir-circuits/gym_verify/src/main.test.nr`:

```rust
#[test]
fn test_within_range() {
    // User inside gym range
    let user_lat = 37423640;
    let user_long = -122084050;
    let gym_lat = 37423642;
    let gym_long = -122084058;
    let max_distance_squared = 1000;

    // Should pass
    main(user_lat, user_long, gym_lat, gym_long, max_distance_squared);
}

#[test(should_fail)]
fn test_outside_range() {
    // User far from gym
    let user_lat = 37423640;
    let user_long = -122084050;
    let gym_lat = 37423642;
    let gym_long = -122084058;
    let max_distance_squared = 10; // Muito próximo para passar

    // Should fail
    main(user_lat, user_long, gym_lat, gym_long, max_distance_squared);
}
```

Execute o teste:
```bash
cd noir-circuits/gym_verify
nargo test
```

### Teste da API

Crie testes básicos em `test_api.py`:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_gyms():
    response = client.get("/gyms")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_generate_proof_valid():
    # Coordenadas próximas (deveria gerar prova válida)
    response = client.post("/generate-proof", json={
        "user_lat": 37423640,
        "user_long": -122084050,
        "gym_lat": 37423642,
        "gym_long": -122084058,
        "max_distance_squared": 1000
    })
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert "proof" in response.json()
```

## Implantação dos Contratos

Crie um script de implantação (`script/Deploy.s.sol`):

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Script} from "forge-std/Script.sol";
import "../src/ZkCheckin.sol";

contract Deploy is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        // Deploy do verificador gerado pelo Noir
        // (Substitua pelo endereço correto do arquivo gerado)
        address verifierAddress = address(0); // Você precisa implantar o verificador primeiro
        
        // Deploy do contrato de check-in
        ZkCheckin checkin = new ZkCheckin(verifierAddress);
        
        // Registrar algumas academias para teste
        checkin.registerGym(1, 37423642, -122084058, 100);
        checkin.registerGym(2, 37422081, -122084438, 150);
        
        vm.stopBroadcast();
    }
}
```

## Cronograma Sugerido

**Dia 1:**
- Configuração do ambiente
- Implementação do circuito Noir
- Testes do circuito

**Dia 2:**
- Desenvolvimento da API FastAPI
- Desenvolvimento dos smart contracts básicos
- Testes de integração

**Dia 3:**
- Deploy dos contratos
- Documentação dos endpoints
- Testes finais e ajustes

## Comunicação com o Frontend

O frontend espera:
1. Um endpoint `/generate-proof` que receba coordenadas e retorne uma prova ZK
2. Um endpoint `/gyms` que retorne a lista de academias disponíveis

Forneça ao desenvolvedor frontend:
- Endereço do contrato implantado
- URL da API
- ABI dos contratos (gerados pelo Foundry)

## O que Ignorar no MVP

- Sistema completo de usuários
- Cálculos complexos de geolocalização (use a aproximação euclidiana)
- Sistema completo de recompensas
- Verificações avançadas anti-fraude

## Recursos Adicionais

- [Documentação do zkVerify](introduction.md)
- [Exemplos de circuitos Noir](examples/)
- [Diagrama da arquitetura](diagrams/)

---

Se surgirem dúvidas, entre em contato imediatamente. O MVP precisa ser entregue em tempo recorde, então foque nas funcionalidades essenciais primeiro. 