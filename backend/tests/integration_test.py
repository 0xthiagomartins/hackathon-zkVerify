import requests
import json
import os
import subprocess
import time
from web3 import Web3
from dotenv import load_dotenv
import pytest

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
API_URL = "http://localhost:8000"
RPC_URL = os.getenv("RPC_URL", "http://localhost:8545")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Configurar Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# Carregar ABI do contrato
with open("../contracts/out/ZkCheckin.sol/ZkCheckin.json", "r") as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)


@pytest.fixture
def generate_proof():
    """Gerar prova ZK para uma academia"""
    # Usar as coordenadas exatas da academia registrada no contrato
    user_lat = 37423642  # Mesma latitude da academia
    user_long = 57915942  # Mesma longitude da academia
    gym_id = 1

    response = requests.post(
        f"{API_URL}/generate-proof",
        json={"user_lat": user_lat, "user_long": user_long, "gym_id": gym_id},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "proof" in data
    assert "public_inputs" in data

    print("✅ Successfully generated ZK proof")
    return data


def test_api_health():
    """Verificar se a API está online"""
    response = requests.get(f"{API_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ API health check passed")


def test_get_gyms():
    """Obter lista de academias"""
    response = requests.get(f"{API_URL}/gyms")
    assert response.status_code == 200
    gyms = response.json()
    assert len(gyms) > 0
    print(f"✅ Retrieved {len(gyms)} gyms from API")
    assert isinstance(gyms, list)


def test_generate_proof(generate_proof):
    """Testar geração de prova"""
    data = generate_proof
    assert data["success"] == True
    assert "proof" in data
    assert "public_inputs" in data


def test_contract_checkin(generate_proof):
    """Testar check-in no contrato usando a prova gerada"""
    try:
        proof_data = generate_proof
        public_inputs = [int(input_val) for input_val in proof_data["public_inputs"]]

        # Debug dos inputs antes de enviar
        print("\nDebug info:")
        print(f"Public inputs being sent: {public_inputs}")

        # Buscar dados da academia diretamente do mapping
        gym_data = contract.functions.gyms(1).call()
        print("Actual gym data from contract:")
        print(f"Latitude: {gym_data[0]}")  # lat
        print(f"Longitude: {gym_data[1]}")  # long
        print(f"Max Distance Squared: {gym_data[2]}")  # maxDistanceSquared
        print(f"Active: {gym_data[3]}")  # active

        # Garantir que a prova seja uma string hexadecimal válida
        proof_hex = proof_data["proof"].replace("0x", "")
        if proof_hex == "...":  # Mock proof
            # Prova mock mais realista
            proof_hex = "00" * 128  # Aumentando para 128 bytes
        proof_bytes = bytes.fromhex(proof_hex)

        print(f"Debug - Proof bytes length: {len(proof_bytes)}")
        print(f"Debug - Public inputs: {public_inputs}")

        # Construir transação
        txn = contract.functions.checkin(
            1, proof_bytes, public_inputs
        ).build_transaction(
            {
                "from": account.address,
                "nonce": w3.eth.get_transaction_count(account.address),
                "gas": 500000,
                "gasPrice": w3.eth.gas_price,
            }
        )

        # Assinar e enviar transação
        signed_txn = w3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        try:
            # Tentar obter o erro da transação
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            if tx_receipt.status == 0:
                # Tentar simular a transação para ver o erro
                w3.eth.call(
                    {
                        "from": account.address,
                        "to": CONTRACT_ADDRESS,
                        "data": txn["data"],
                        "gas": txn["gas"],
                    }
                )
        except Exception as call_error:
            print(f"Debug - Transaction error details: {str(call_error)}")
            raise

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        assert receipt.status == 1, "Transaction failed"
        print(f"✅ Check-in transaction successful: {receipt.transactionHash.hex()}")

        # Verificar check-in no contrato
        checkin_count = contract.functions.getUserGymCheckins(account.address, 1).call()
        assert checkin_count > 0, "Check-in count should be greater than 0"
        print(f"✅ User now has {checkin_count} check-ins at gym 1")

    except Exception as e:
        print(f"❌ Error during contract check-in: {str(e)}")
        raise


if __name__ == "__main__":
    pytest.main([__file__])
