# Sprint 2: Tarefas e Status

## Gestão de Status
- 🔴 Não iniciado
- 🟡 Em andamento
- 🟢 Concluído
- ⛔ Bloqueado (incluir motivo)

## Estrutura Básica da API

| Tarefa | Status | Observações |
|--------|--------|-------------|
| Configurar projeto FastAPI | 🟢 | Configurado em src/main.py |
| Implementar estrutura de pastas (routers, models, etc.) | 🟢 | Estrutura completa |
| Configurar middleware CORS | 🟢 | Em main.py |
| Implementar sistema básico de logging | 🟢 | Debug logs implementados |
| Configurar handler para erros centralizados | 🟢 | HTTPException configurado |
| Criar modelos Pydantic para validação de dados | 🟢 | Em models/gym.py |
| Implementar mecanismo de configuração via variáveis de ambiente | 🟢 | Em core/config.py |

## Endpoints para Academias

| Tarefa | Status | Observações |
|--------|--------|-------------|
| Definir modelo de dados para academia | 🟢 | Em models/gym.py |
| Implementar endpoint GET /gyms | 🟢 | Em routes/gyms.py |
| Implementar endpoint GET /gym/{gym_id} | 🟢 | Em routes/gyms.py |
| Criar dados mock para academias de teste | 🟢 | Em tests/test_api.py |
| Adicionar validação para parâmetros de entrada | 🟢 | Via Pydantic |

## Geração de Provas ZK

| Tarefa | Status | Observações |
|--------|--------|-------------|
| Definir modelo para requisição de prova | 🟢 | ProofRequest em models/gym.py |
| Criar endpoint POST /generate-proof | 🟢 | Em routes/proofs.py |
| Implementar integração com circuito Noir | 🟡 | Em progresso |
| Criar função helper para executar Nargo | 🟢 | Em routes/proofs.py |
| Implementar lógica para manipulação de arquivos de prova | 🟢 | Em routes/proofs.py |
| Adicionar tratamento para falhas na geração | 🟢 | Try/catch implementado |

## Testes e Documentação

| Tarefa | Status | Observações |
|--------|--------|-------------|
| Configurar pytest para ambiente de teste | 🟢 | pytest.ini configurado |
| Criar testes para endpoints de academias | 🟢 | Em tests/test_api.py |
| Criar testes para geração de provas | 🟢 | Em tests/test_api.py |
| Configurar documentação automática com Swagger UI | 🟢 | FastAPI docs ativado |
