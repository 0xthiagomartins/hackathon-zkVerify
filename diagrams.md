# Diagramas de Arquitetura - zkVerify MVP

Este documento contém os diagramas da arquitetura do MVP do zkVerify, mostrando os fluxos de comunicação entre os diversos componentes do sistema.

## 1. Visão Geral da Arquitetura

```mermaid
flowchart TB
    subgraph "Frontend"
        UI["Interface do Usuário (Next.js)"]
        WI["Integração com Carteira (ethers.js)"]
        Map["Componente de Mapa (Leaflet)"]
    end
    subgraph "Backend"
        API["API (FastAPI)"]
        ZKP["Gerador de Provas ZK (Noir)"]
        DB["Banco de Dados (Sqlite)"]
    end
    subgraph "Blockchain"
        SC["Smart Contracts (Solidity)"]
        VC["Verificador ZK"]
        GM["GymManager"]
        VN["VoucherNFT"]
    end
    UI --> Map
    UI --> WI
    WI --> SC
    UI --> API
    API --> ZKP
    API --> DB
    ZKP --> API
    API --> SC
    SC --> VC
    VC --> GM
    GM --> VN
    classDef frontend fill:#d4f1f9,stroke:#05a,stroke-width:2px
    classDef backend fill:#e1d4e6,stroke:#70c,stroke-width:2px
    classDef blockchain fill:#ffecb3,stroke:#e65c00,stroke-width:2px
    class UI,WI,Map frontend
    class API,ZKP,DB backend
    class SC,VC,GM,VN blockchain
```

## 2. Fluxo de Check-in

```mermaid
sequenceDiagram
    actor User as Usuário
    participant App as App Móvel
    participant API as Backend API
    participant ZKP as Gerador de Provas ZK
    participant SC as Smart Contracts
    participant BC as Blockchain
    
    User->>App: Seleciona academia
    User->>App: Solicita check-in
    App->>App: Obtém localização GPS
    App->>API: Envia coordenadas e ID da academia
    API->>ZKP: Solicita geração de prova ZK
    ZKP->>ZKP: Executa circuito Noir
    ZKP-->>API: Retorna prova ZK e inputs públicos
    API-->>App: Envia prova ZK e inputs públicos
    App->>App: Solicita conexão com carteira
    App->>SC: Envia transação com prova ZK
    SC->>SC: Verifica prova ZK
    SC->>BC: Registra check-in se prova válida
    BC-->>SC: Confirma transação
    SC-->>App: Retorna resultado
    App-->>User: Exibe confirmação de check-in
```

## 3. Componentes do Sistema

```mermaid
flowchart LR
    subgraph "Frontend Components"
        direction TB
        CheckInPage[Check-in Page]
        MapComponent[Map Component]
        WalletConnect[Wallet Connector]
        StatusIndicator[Status Indicator]
    end
    
    subgraph "Backend Components"
        direction TB
        RESTApi[REST API Controller]
        ProofService[ZK Proof Service]
        GymService[Gym Management Service]
        NoirWrapper[Noir Circuit Wrapper]
    end
    
    subgraph "Smart Contracts"
        direction TB
        ZkCheckin[ZkCheckin Contract]
        NoirVerifier[Noir Verifier Contract]
        GymRegistry[Gym Registry]
        ProofValidator[Proof Validator]
    end
    
    CheckInPage --> MapComponent
    CheckInPage --> WalletConnect
    CheckInPage --> StatusIndicator
    
    WalletConnect --> ZkCheckin
    
    CheckInPage --> RESTApi
    RESTApi --> ProofService
    ProofService --> NoirWrapper
    RESTApi --> GymService
    
    ZkCheckin --> NoirVerifier
    ZkCheckin --> GymRegistry
    NoirVerifier --> ProofValidator
    
    classDef frontend fill:#d4f1f9,stroke:#05a,stroke-width:1px
    classDef backend fill:#e1d4e6,stroke:#70c,stroke-width:1px
    classDef contracts fill:#ffecb3,stroke:#e65c00,stroke-width:1px
    
    class CheckInPage,MapComponent,WalletConnect,StatusIndicator frontend
    class RESTApi,ProofService,GymService,NoirWrapper backend
    class ZkCheckin,NoirVerifier,GymRegistry,ProofValidator contracts
```

## 4. Fluxo de Dados Detalhado

```mermaid
flowchart TB
    UserLocation["Localização do Usuário\n(Lat/Long)"] --> InputPreparation["Preparação de Entrada\n(Conversão para formato do circuito)"]
    GymLocation["Localização da Academia\n(Lat/Long)"] --> InputPreparation
    MaxDistance["Distância Máxima Permitida"] --> InputPreparation
    Timestamp["Timestamp Atual"] --> InputPreparation
    
    InputPreparation --> NoirCircuit["Circuito Noir\n(simple_location_verify.nr)"]
    NoirCircuit --> ZKProof["Prova ZK Gerada"]
    NoirCircuit --> PublicInputs["Inputs Públicos\n(Parâmetros verificáveis)"]
    
    ZKProof --> SmartContract["Smart Contract\n(ZkCheckin.sol)"]
    PublicInputs --> SmartContract
    
    SmartContract --> VerifyResult{"Prova Válida?"}
    VerifyResult -->|Sim| RegisterCheckIn["Registrar Check-in\nem VoucherNFT"]
    VerifyResult -->|Não| RejectCheckIn["Rejeitar Check-in"]
    
    RegisterCheckIn --> DCPSystem["Sistema DCP\n(Transferir pontos para academia)"]
    
    classDef inputs fill:#e1f5fe,stroke:#0288d1,stroke-width:1px
    classDef processing fill:#e8f5e9,stroke:#388e3c,stroke-width:1px
    classDef outputs fill:#fff3e0,stroke:#f57c00,stroke-width:1px
    classDef decision fill:#fce4ec,stroke:#d81b60,stroke-width:1px
    
    class UserLocation,GymLocation,MaxDistance,Timestamp inputs
    class InputPreparation,NoirCircuit,SmartContract processing
    class ZKProof,PublicInputs,RegisterCheckIn,RejectCheckIn outputs
    class VerifyResult decision
```

## 5. Arquitetura de Implantação

```mermaid
flowchart TB
    subgraph "Infraestrutura Frontend"
        Vercel["Vercel\n(Next.js App)"]
    end
    
    subgraph "Infraestrutura Backend"
        EC2["AWS EC2\n(API + Noir)"]
        RDS["AWS RDS\n(PostgreSQL)"]
    end
    
    subgraph "Infraestrutura Blockchain"
        TestNet["Testnet\n(Sepolia/Mumbai)"]
    end
    
    Browser["Navegador do Usuário"] --> Vercel
    Vercel --> EC2
    EC2 --> RDS
    Vercel --> TestNet
    EC2 --> TestNet
    Wallet["Carteira do Usuário\n(MetaMask)"] --> TestNet
    
    classDef user fill:#ffebee,stroke:#c62828,stroke-width:1px
    classDef frontend fill:#d4f1f9,stroke:#05a,stroke-width:1px
    classDef backend fill:#e1d4e6,stroke:#70c,stroke-width:1px
    classDef blockchain fill:#ffecb3,stroke:#e65c00,stroke-width:1px
    
    class Browser,Wallet user
    class Vercel frontend
    class EC2,RDS backend
    class TestNet blockchain
```

## 6. Fluxo Completo do Check-in com ZK Proofs

```mermaid
sequenceDiagram
    actor User as Usuário
    participant Browser as Navegador
    participant Frontend as Frontend Next.js
    participant Backend as Backend API
    participant Noir as Gerador de Provas Noir
    participant Wallet as MetaMask
    participant Contract as ZkCheckin Contract
    participant Verifier as NoirVerifier
    
    User->>Browser: Acessa aplicativo
    Browser->>Frontend: Carrega interface
    Frontend->>Backend: GET /gyms
    Backend->>Frontend: Lista de academias
    
    User->>Frontend: Seleciona academia
    User->>Frontend: Clica em "Check-in"
    Frontend->>Browser: Solicita permissão de geolocalização
    Browser->>User: Pede autorização
    User->>Browser: Autoriza acesso à localização
    Browser->>Frontend: Retorna coordenadas GPS
    
    Frontend->>Backend: POST /generate-proof
    Note over Frontend,Backend: Envia coordenadas do usuário e academia
    
    Backend->>Noir: Prepara inputs para o circuito
    Noir->>Noir: Gera prova ZK
    Noir->>Backend: Retorna prova e inputs públicos
    Backend->>Frontend: Retorna prova ZK
    
    Frontend->>Wallet: Solicita conexão
    Wallet->>User: Pede aprovação
    User->>Wallet: Aprova conexão
    Wallet->>Frontend: Retorna conta conectada
    
    Frontend->>Wallet: Solicita transação
    Note over Frontend,Wallet: checkin(gymId, proof, publicInputs)
    
    Wallet->>User: Mostra detalhes da transação
    User->>Wallet: Confirma transação
    Wallet->>Contract: Envia transação
    
    Contract->>Verifier: verify(proof, publicInputs)
    Verifier->>Contract: Retorna resultado (verdadeiro/falso)
    
    alt Prova válida
        Contract->>Contract: Registra check-in
        Contract->>Wallet: Transação bem-sucedida
    else Prova inválida
        Contract->>Wallet: Transação falha
    end
    
    Wallet->>Frontend: Retorna resultado
    Frontend->>User: Exibe resultado do check-in
```

## 7. Arquitetura do Circuito Noir

```mermaid
flowchart LR
    subgraph "Entradas Privadas"
        UserLat["Latitude do Usuário"]
        UserLong["Longitude do Usuário"]
    end
    
    subgraph "Entradas Públicas"
        GymLat["Latitude da Academia"]
        GymLong["Longitude da Academia"]
        MaxDistSq["Distância Max Quadrada"]
        CurrTime["Timestamp Atual"]
        ProofTime["Timestamp da Prova"]
    end
    
    subgraph "Circuito Noir"
        CalcDiff["Calcular Diferença\nLat/Long"]
        CalcDistSq["Calcular Distância\nQuadrada"]
        CompDist["Comparar com\nDistância Máxima"]
        CalcTimeDiff["Calcular Diferença\nde Tempo"]
        CompTime["Comparar com\nTempo Máximo"]
        FinalConstraint["Aplicar\nConstraints"]
    end
    
    UserLat --> CalcDiff
    UserLong --> CalcDiff
    GymLat --> CalcDiff
    GymLong --> CalcDiff
    
    CalcDiff --> CalcDistSq
    CalcDistSq --> CompDist
    MaxDistSq --> CompDist
    
    CurrTime --> CalcTimeDiff
    ProofTime --> CalcTimeDiff
    CalcTimeDiff --> CompTime
    
    CompDist --> FinalConstraint
    CompTime --> FinalConstraint
    
    FinalConstraint --> ValidProof["Prova Válida\n(ou Falha)"]
    
    classDef private fill:#e8eaf6,stroke:#3949ab,stroke-width:1px
    classDef public fill:#fff8e1,stroke:#ff8f00,stroke-width:1px
    classDef circuit fill:#e0f2f1,stroke:#00796b,stroke-width:1px
    classDef output fill:#f9fbe7,stroke:#9e9d24,stroke-width:1px
    
    class UserLat,UserLong private
    class GymLat,GymLong,MaxDistSq,CurrTime,ProofTime public
    class CalcDiff,CalcDistSq,CompDist,CalcTimeDiff,CompTime,FinalConstraint circuit
    class ValidProof output
```

## 8. Integração com os Sistemas Existentes (Fase 2)

```mermaid
flowchart TB
    subgraph "Sistema zkVerify"
        ZkCheckin["ZkCheckin Contract"]
        NoirVerifier["NoirVerifier"]
    end
    
    subgraph "Sistema Core DeGym"
        CheckinContract["Checkin.sol"]
        VoucherNFT["VoucherNFT.sol"]
        GymNFT["GymNFT.sol"]
        Treasury["Treasury.sol"]
    end
    
    ZkCheckin -->|"Integração\n(Fase 2)"| CheckinContract
    CheckinContract --> VoucherNFT
    CheckinContract --> GymNFT
    GymNFT --> Treasury
    
    classDef zkverify fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef core fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    
    class ZkCheckin,NoirVerifier zkverify
    class CheckinContract,VoucherNFT,GymNFT,Treasury core
```

## Comunicação entre os Componentes

A arquitetura do MVP do zkVerify foi projetada para permitir a verificação de presença física de usuários nas academias de forma privada e segura, utilizando provas de conhecimento zero. Os fluxos de comunicação são:

1. **App Mobile → Backend API**: Envia dados de geolocalização e solicita geração de prova ZK
2. **Backend → Noir**: Gera provas criptográficas que validam presença sem revelar localização exata
3. **App Mobile → Smart Contract**: Envia a prova gerada para verificação on-chain
4. **Smart Contract → Verificador ZK**: Valida matematicamente a prova
5. **Smart Contract → Sistema Core DeGym**: Registra check-in válido e distribui recompensas

Este design permite uma separação clara de responsabilidades, mantendo a privacidade do usuário em primeiro plano enquanto garante a integridade do sistema de check-in. 