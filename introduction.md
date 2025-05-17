# zkVerify: Introdução

## O que é o zkVerify?

O zkVerify é o componente de verificação do DeGym que utiliza tecnologia de provas de conhecimento zero (Zero-Knowledge Proofs) para confirmar a presença física dos usuários nas academias sem comprometer sua privacidade. É como um "carimbo digital" que prova que você está realmente na academia, sem revelar sua localização exata.

## O Problema que Resolvemos

As academias enfrentam um desafio fundamental: como verificar que os usuários estão fisicamente presentes para autorizar check-ins, sem implementar sistemas invasivos de monitoramento? Ao mesmo tempo, os usuários valorizam sua privacidade e não querem seus movimentos rastreados constantemente.

Sistemas tradicionais apresentam problemas:
- **Catracas físicas**: Facilmente burladas (emprestar cartões)
- **Geolocalização simples**: Comprometem a privacidade do usuário
- **QR Codes**: Podem ser compartilhados ou falsificados
- **Check-ins manuais**: Sujeitos a fraudes e erros

## Como o zkVerify Funciona (Explicação Simplificada)

Imagine que você precisa provar que está dentro de um círculo (a academia), sem revelar exatamente onde você está nesse círculo. O zkVerify faz exatamente isso:

1. **Captação de dados**: O aplicativo obtém sua localização GPS
2. **Geração de prova**: Seu dispositivo cria uma "prova matemática" que confirma que você está dentro do perímetro da academia, sem revelar suas coordenadas exatas
3. **Verificação da prova**: A blockchain verifica a matemática da prova, sem ver os dados originais
4. **Check-in confirmado**: Se a prova for válida, o check-in é registrado e você recebe seus pontos DCP

![Processo Simplificado](diagrams/zkVerify_simplified.png)

## Benefícios para Todos

### Para Usuários
- **Privacidade preservada**: Sua localização exata nunca é compartilhada
- **Verificação rápida**: O processo leva apenas segundos
- **Controle total**: Você decide quando iniciar o processo
- **Sem hardware adicional**: Funciona com o smartphone que você já possui

### Para Academias
- **Dados confiáveis**: Check-ins verificados matematicamente
- **Sem infraestrutura adicional**: Não requer catracas ou hardware especializado
- **Anti-fraude**: Praticamente impossível de falsificar
- **Métricas precisas**: Dados reais de frequência para tomada de decisões

## Zero-Knowledge Proofs: Explicação Simples

Zero-Knowledge Proofs (ZKPs) são como resolver um quebra-cabeça em uma sala fechada e convencer alguém fora da sala que você sabe a solução, sem mostrar o quebra-cabeça ou a solução.

**Exemplo do mundo real**: Imagine que você queira provar a um amigo daltônico que duas bolas têm cores diferentes, sem revelar quais são as cores:

1. Seu amigo coloca as bolas atrás das costas
2. Ele pode trocar as bolas de mão ou não
3. Você consegue dizer se ele trocou as bolas
4. Repetindo isso várias vezes, você prova que pode distinguir as bolas sem revelar as cores

No DeGym, provamos "estou dentro da academia" sem revelar "estou exatamente aqui".

## Fluxo de Check-in Detalhado

1. **Abertura do aplicativo**: Usuário abre o app DeGym dentro da academia
2. **Seleção da academia**: Usuário escolhe a academia onde está
3. **Inicialização do check-in**: Usuário pressiona o botão "Check-in"
4. **Permissão de localização**: App solicita permissão temporária de localização
5. **Processamento em segundo plano**:
   - App obtém coordenadas GPS
   - Circuito Noir gera a prova ZK localmente
   - Apenas a prova (não as coordenadas) é enviada para a blockchain
6. **Verificação on-chain**:
   - Smart contract verifica a validade matemática da prova
   - Voucher e pontos DCP são verificados
7. **Confirmação**: Usuário recebe notificação de check-in bem-sucedido
8. **Recompensa**: Pontos DCP são atribuídos conforme o voucher

## Segurança e Privacidade

O zkVerify foi projetado com segurança em camadas:

- **Provas não-falsificáveis**: Matematicamente impossível de forjar
- **Proteção contra replay**: Cada prova inclui um timestamp único
- **Privacidade por design**: Apenas a informação mínima necessária é compartilhada
- **Processamento local**: Os dados sensíveis nunca saem do dispositivo do usuário

## Tecnologias Utilizadas

O zkVerify é construído sobre:

- **Noir**: Linguagem especializada para circuitos ZK
- **Taraxa Blockchain**: Para verificação das provas e registro dos check-ins
- **Web3**: Para interação com smart contracts
- **FastAPI**: Backend para processamento de provas (quando necessário)

## Próximos Passos

Na primeira fase do MVP, estamos focando na verificação básica de presença. Nas fases futuras, planejamos:

- Triangulação com beacons Bluetooth para maior precisão em ambientes fechados
- Verificação de padrões de movimento para confirmar que o usuário está realmente se exercitando
- Integração com wearables para enriquecimento de dados de atividade física
- Sistema de reputação para academias baseado em verificações bem-sucedidas

---

**Nota para Desenvolvedores**: Para detalhes técnicos mais profundos sobre a implementação, consulte o arquivo [README.md](README.md) principal e os exemplos de código no diretório `examples/`. 