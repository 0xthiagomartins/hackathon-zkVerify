# Instruções para Desenvolvedor Frontend - DeGym zkVerify MVP

## Visão Geral

Você está entrando no projeto DeGym, uma plataforma descentralizada para academias. Sua tarefa é desenvolver o **frontend do MVP do componente zkVerify**, que permite verificar a presença dos usuários nas academias usando provas de conhecimento zero (para preservar privacidade).

**O objetivo simples**: Criar uma interface onde o usuário pode selecionar uma academia, obter sua localização atual, e fazer check-in de forma segura.

## Tecnologias que Você Vai Usar

- **Next.js** com TypeScript
- **ethers.js** (v5.7.2) para integração com blockchain
- **Leaflet** para mapas (ou Google Maps API)
- **Axios** para chamadas de API
- **TailwindCSS** para estilos (opcional, mas recomendado)

## Configuração do Ambiente (30 minutos)

```bash
# Criar novo projeto Next.js
npx create-next-app@latest frontend --typescript
cd frontend

# Instalar dependências
npm install ethers@5.7.2 axios
npm install leaflet react-leaflet
npm install -D @types/leaflet

# Opcional: TailwindCSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Configure o `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CONTRACT_ADDRESS=0x... # Será fornecido pelo dev de backend
```

## O que Você Precisa Desenvolver (1-2 dias)

### 1. Tela de Check-in (Prioridade Máxima)

Crie uma página principal (`pages/index.tsx`) com:

- Mapa mostrando a localização do usuário e academias próximas
- Lista de academias disponíveis (inicialmente mockadas)
- Botão "Check-in" que:
  1. Solicita permissão de localização
  2. Chama a API de backend para gerar a prova ZK 
  3. Envia a prova para o contrato na blockchain
  4. Mostra o status do check-in

**Exemplo Simplificado:**

```tsx
// pages/index.tsx
import { useState, useEffect } from 'react';
import axios from 'axios';
import { ethers } from 'ethers';
import Map from '../components/Map'; // Você criará esse componente

export default function CheckinPage() {
  const [selectedGym, setSelectedGym] = useState(null);
  const [location, setLocation] = useState(null);
  const [checkingIn, setCheckingIn] = useState(false);
  const [status, setStatus] = useState('idle');
  
  // Obter localização do usuário
  const getLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
        },
        (error) => {
          console.error("Erro ao obter localização:", error);
          alert("Por favor, habilite a localização para fazer check-in");
        }
      );
    } else {
      alert("Geolocalização não suportada neste navegador");
    }
  };
  
  // Processar check-in
  const handleCheckin = async () => {
    if (!selectedGym || !location) return;
    
    try {
      setCheckingIn(true);
      setStatus('processing');
      
      // 1. Gerar prova ZK no backend
      const proofResponse = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/generate-proof`, {
        user_lat: Math.round(location.lat * 1000000), 
        user_long: Math.round(location.lng * 1000000),
        gym_lat: selectedGym.lat,
        gym_long: selectedGym.long,
        max_distance_squared: selectedGym.maxDistance * selectedGym.maxDistance
      });
      
      // 2. Conectar à carteira
      await window.ethereum.request({ method: 'eth_requestAccounts' });
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const signer = provider.getSigner();
      
      // 3. Criar instância do contrato
      const contract = new ethers.Contract(
        process.env.NEXT_PUBLIC_CONTRACT_ADDRESS,
        ['function checkin(uint256 gymId, bytes memory proof, uint256[] memory publicInputs)'],
        signer
      );
      
      // 4. Enviar transação
      const tx = await contract.checkin(
        selectedGym.id,
        proofResponse.data.proof,
        proofResponse.data.public_inputs.map(input => ethers.BigNumber.from(input))
      );
      
      await tx.wait();
      setStatus('success');
      
    } catch (error) {
      console.error("Erro no check-in:", error);
      setStatus('error');
    } finally {
      setCheckingIn(false);
    }
  };
  
  // Mock de academias para o MVP
  const gyms = [
    { id: 1, name: "Academia Central", lat: 37423642, long: -122084058, maxDistance: 100 },
    { id: 2, name: "Fitness Plus", lat: 37422081, long: -122084438, maxDistance: 150 }
  ];
  
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">DeGym Check-in</h1>
      
      {/* Componente de Mapa */}
      <div className="mb-4" style={{ height: '400px' }}>
        <Map 
          userLocation={location} 
          gyms={gyms}
          onSelectGym={setSelectedGym}
          selectedGym={selectedGym}
        />
      </div>
      
      {/* Seleção de Academia */}
      <div className="mb-4">
        <label className="block mb-2">Selecione uma academia:</label>
        <select 
          className="w-full p-2 border rounded"
          value={selectedGym?.id || ''}
          onChange={(e) => {
            const gymId = Number(e.target.value);
            setSelectedGym(gyms.find(g => g.id === gymId) || null);
          }}
        >
          <option value="">Selecione uma academia</option>
          {gyms.map(gym => (
            <option key={gym.id} value={gym.id}>{gym.name}</option>
          ))}
        </select>
      </div>
      
      {/* Botões de Ação */}
      <div className="flex gap-4">
        <button 
          className="px-4 py-2 bg-blue-500 text-white rounded"
          onClick={getLocation}
        >
          Obter Localização
        </button>
        
        <button 
          className="px-4 py-2 bg-green-500 text-white rounded"
          onClick={handleCheckin}
          disabled={!selectedGym || !location || checkingIn}
        >
          {checkingIn ? 'Processando...' : 'Fazer Check-in'}
        </button>
      </div>
      
      {/* Status */}
      {status === 'success' && (
        <div className="mt-4 p-2 bg-green-100 text-green-800 rounded">
          Check-in realizado com sucesso!
        </div>
      )}
      
      {status === 'error' && (
        <div className="mt-4 p-2 bg-red-100 text-red-800 rounded">
          Erro ao fazer check-in. Tente novamente.
        </div>
      )}
    </div>
  );
}
```

### 2. Componente de Mapa (meio-dia)

Crie um componente de mapa (`components/Map.tsx`) para exibir:
- Localização do usuário
- Academias próximas com seus perímetros de check-in
- Interação para selecionar academia

### 3. Integração com Carteira (meio-dia)

Adicione componente de conexão de carteira (Metamask) para permitir transações.

## Cronograma Sugerido

**Dia 1:**
- Configuração do ambiente
- Criação do layout básico
- Implementação do componente de mapa

**Dia 2:**
- Integração com carteira
- Implementação da lógica de check-in
- Testes e ajustes

## Comunicação com o Backend

Para o MVP, o backend fornecerá:

1. Endpoint para gerar prova ZK: `POST /generate-proof`
2. Endpoint para obter academias: `GET /gyms`

O backend será responsável pela parte pesada de gerar a prova ZK. Você só precisa enviar os dados e receber a prova gerada.

## O que Ignorar no MVP

- Sistema completo de usuários e autenticação
- Histórico de check-ins
- Dashboard detalhado
- Sistemas de recompensas

## Recursos Adicionais

- [Documentação do zkVerify](introduction.md)
- [Exemplos de contratos](examples/)
- [Diagrama da arquitetura](diagrams/)

---

Se surgirem dúvidas, entre em contato imediatamente. O MVP precisa ser entregue em tempo recorde, então foque nas funcionalidades essenciais primeiro. 