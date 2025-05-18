# Status das Sprints - Atualizado

### ✅ Concluído
1. **Circuito Noir**
   - Implementação do circuito básico de verificação de distância
   - Testes do circuito implementados
   - Compilação gerando ABI corretamente
   - Conversão de coordenadas negativas implementada

2. **API Básica**
   - Endpoints básicos implementados
   - Integração com o circuito Noir
   - Modelos de dados definidos
   - Mock de dados das academias

### 🏗️ Em Progresso
1. **Integração com Contrato**
   - Gerar verificador Solidity para o circuito ⬅️ **(Próximo passo)**
   - Integrar verificador com o contrato principal
   - Atualizar deploy script

2. **Geração de Provas**
   - Ajustar geração de provas na API
   - Integrar com o novo verificador
   - Implementar cache de provas

### ⏳ Pendente
1. **Otimizações**
   - Otimizar consumo de gas
   - Melhorar performance da API
   - Implementar timeout para geração de provas

2. **Testes e Documentação**
   - Testes de integração end-to-end
   - Documentação técnica completa
   - Exemplos de uso da API
   - Documentar limitações do circuito

### 🐛 Bugs Conhecidos
1. ~~Erro de imports no remappings.txt~~ *(Resolvido)*
2. ~~Public inputs zerados~~ *(Resolvido)*
3. ~~Integração API-circuito~~ *(Resolvido)*
4. Verificador Solidity pendente 