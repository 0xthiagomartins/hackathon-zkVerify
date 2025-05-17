# Sprint 2: Implementação do Mapa

## Objetivos

Nesta sprint, o foco será na implementação do componente de mapa interativo, uma parte essencial do aplicativo que permitirá aos usuários visualizar sua localização em relação às academias disponíveis. O mapa será a principal forma de interação visual para o processo de check-in.

## Metas Específicas

1. **Integração com Biblioteca de Mapas**
   - Integrar Leaflet (ou Google Maps API) ao projeto
   - Configurar mapa básico com controles de zoom e navegação
   - Implementar carregamento otimizado do mapa

2. **Funcionalidades do Mapa**
   - Exibir localização atual do usuário com marcador personalizado
   - Mostrar academias próximas com marcadores distintos
   - Visualizar perímetros de check-in das academias (círculos de distância)
   - Implementar interatividade para seleção de academia via mapa

3. **Integração com Componentes Existentes**
   - Sincronizar seleção no mapa com o dropdown de academias
   - Atualizar mapa quando a localização do usuário for obtida
   - Adicionar indicação visual quando usuário estiver dentro do perímetro válido

## Critérios de Aceitação

- Mapa carregando corretamente e exibindo a área geográfica relevante
- Marcadores de usuário e academias visualmente distintos
- Perímetros de check-in claramente visíveis
- Interação entre mapa e seleção de academia funcionando nos dois sentidos
- Mapa responsivo em diferentes tamanhos de tela
- Desempenho adequado (sem lentidão no carregamento ou interação) 