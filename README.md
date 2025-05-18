# zkVerify Hackathon powered by NearX

# ZKCheckin

ZKCheckin é um sistema de verificação de presença em academias que utiliza provas de conhecimento zero (Zero Knowledge Proofs) para garantir a privacidade dos usuários enquanto comprova sua presença física no local.

## Como Funciona

1. O usuário envia suas coordenadas GPS
2. O sistema gera uma prova ZK que verifica se o usuário está dentro do perímetro da academia
3. A prova é verificada on-chain, registrando o check-in sem revelar a localização exata do usuário

## Tecnologias

- **Noir**: Linguagem para circuitos ZK
- **Barretenberg**: Backend de prova
- **FastAPI**: API REST
- **Solidity**: Smart Contracts
- **Docker**: Containerização

## Características

- ✨ Privacidade preservada através de ZK proofs
- 🔒 Verificação on-chain
- 🌍 Suporte a coordenadas GPS
- ⚡ API REST para integração
- 🐳 Containerizado para fácil deploy

