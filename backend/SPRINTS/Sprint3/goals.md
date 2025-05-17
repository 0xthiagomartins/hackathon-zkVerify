# Sprint 3: Desenvolvimento dos Smart Contracts

## Objetivos

Nesta sprint, o foco será no desenvolvimento e testes dos smart contracts que interagirão com as provas ZK geradas pelo backend. Os contratos permitirão o registro de academias e a verificação de check-ins com provas ZK.

## Metas Específicas

1. **Preparação do Ambiente de Contratos**
   - Configurar projeto Foundry com estrutura adequada
   - Importar dependências necessárias (OpenZeppelin, etc.)
   - Configurar ambiente de testes para contratos
   - Estruturar arquitetura dos contratos

2. **Implementação do Contrato ZkCheckin**
   - Desenvolver contrato principal de check-in com integração ZK
   - Implementar funções para registro de academias
   - Criar sistema de verificação de provas
   - Implementar armazenamento de dados de check-in

3. **Integração com Verificador Noir**
   - Importar e integrar verificador gerado pelo Noir
   - Implementar interface para comunicação entre contratos
   - Testar verificação de provas válidas e inválidas
   - Otimizar consumo de gas para operações de verificação

4. **Testes e Documentação dos Contratos**
   - Desenvolver testes abrangentes para todos os cenários
   - Implementar testes de fuzzing para casos extremos
   - Documentar interfaces e funções dos contratos
   - Analisar segurança e otimizações

## Critérios de Aceitação

- Contratos compilando sem erros ou warnings
- Testes abrangentes cobrindo todas as funcionalidades
- Integração com verificador Noir funcionando corretamente
- Análise de gas otimizada para operações críticas
- Documentação clara das interfaces para integração frontend
- Script de deploy configurado e testado 