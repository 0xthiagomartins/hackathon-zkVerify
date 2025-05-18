# Sprint 3: Tarefas e Status

## Gestão de Status
- 🔴 Não iniciado
- 🟡 Em andamento
- 🟢 Concluído
- ⛔ Bloqueado (incluir motivo)

## Preparação do Ambiente de Contratos

| Tarefa | Status | Observações |
|--------|--------|-------------|
| Configurar projeto Foundry | 🟢 | Configurado e funcionando |
| Instalar dependências (OpenZeppelin) | 🟢 | Importado em ZkCheckin.sol |
| Configurar .gitignore para arquivos de build | 🟢 | Configurado |
| Estruturar diretórios (src, test, script) | 🟢 | Estrutura completa |
| Definir versão de Solidity a ser utilizada | 🟢 | ^0.8.20 |
| Configurar foundry.toml com parâmetros adequados | 🟢 | Configurado |

## Implementação do Contrato ZkCheckin

| Tarefa | Status | Observações |
|--------|--------|-------------|
| Criar estrutura básica do contrato ZkCheckin | 🟢 | Em ZkCheckin.sol |
| Implementar estrutura de dados Gym | 🟢 | Struct implementada |
| Desenvolver função registerGym | 🟢 | Função implementada |
| Implementar mapeamento de academias e check-ins | 🟢 | Mappings configurados |
| Criar função checkin com verificação de provas | 🟢 | Implementado |
| Adicionar eventos para ações importantes | 🟢 | Eventos definidos |
| Implementar controle de acesso com Ownable | 🟢 | Herança configurada |

## Integração com Verificador Noir

| Tarefa | Status | Observações |
|--------|--------|-------------|
| Importar contrato de verificador gerado | 🟡 | Interface criada |
| Criar interface para o verificador | 🟢 | INoirVerifier.sol |
| Implementar chamada ao verificador no checkin | 🟢 | Em ZkCheckin.sol |
| Testar integração com diferentes tipos de prova | 🟡 | Em progresso |
| Implementar tratamento de erros de verificação | 🟢 | Requires implementados |

## Testes e Documentação

| Tarefa | Status | Observações |
|--------|--------|-------------|
| Criar testes para registro de academias | 🟢 | Em ZkCheckin.t.sol |
| Implementar testes para verificação de provas | 🟢 | Testes implementados |
| Testar casos de erro (provas inválidas, etc.) | 🟢 | Testes de revert |
| Adicionar testes de fuzzing para dados aleatórios | 🔴 | Pendente |
| Documentar interfaces dos contratos | 🟢 | Documentação inline |
| Criar ABI para integração com frontend | 🟢 | ABI gerado |
| Desenvolver script de deploy | 🟢 | Em Deploy.s.sol | 