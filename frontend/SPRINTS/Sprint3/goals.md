# Sprint 3: Integração com Carteira e API

## Objetivos

Nesta sprint, o foco será integrar a aplicação com carteiras blockchain (MetaMask) e com a API de backend que gera as provas de conhecimento zero. Esta é a fase principal de funcionalidade, onde implementaremos o fluxo completo de check-in com verificação ZK.

## Metas Específicas

1. **Integração com Carteira (Wallet)**
   - Implementar componente de conexão à carteira MetaMask
   - Criar sistema de gerenciamento de estado para a conexão da carteira
   - Lidar com diferentes redes blockchain e solicitações de mudança de rede
   - Implementar feedback visual do status da conexão

2. **Integração com API de Backend**
   - Configurar cliente Axios para comunicação com API
   - Implementar chamada ao endpoint `/gyms` para obter lista de academias
   - Criar função para solicitar geração de prova ZK via `/generate-proof`
   - Lidar com erros e timeouts de API

3. **Fluxo de Check-in**
   - Implementar fluxo completo de check-in:
     - Obter localização do usuário
     - Validar proximidade com a academia
     - Solicitar geração de prova ZK
     - Enviar transação para o smart contract
   - Implementar feedback visual durante cada etapa do processo
   - Criar sistema de notificação para sucesso/erro no check-in

## Critérios de Aceitação

- Conexão com MetaMask funcionando corretamente
- Obtenção da lista de academias da API
- Solicitação e recebimento de provas ZK funcionando
- Envio de transações para o smart contract
- Feedback visual adequado durante todo o processo
- Tratamento adequado de erros em cada etapa
- Fluxo completo de check-in funcional 