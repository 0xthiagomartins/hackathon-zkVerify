import requests
import json
import os
import subprocess
import time
from web3 import Web3
from dotenv import load_dotenv

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
with open("../../contracts/out/ZkCheckin.sol/ZkCheckin.json", "r") as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)


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
    return gyms


def test_generate_proof(gym_id=1):
    """Gerar prova ZK para uma academia"""
    # Coordenadas próximas à academia
    user_lat = 37423640
    user_long = -122084050

    response = requests.post(
        f"{API_URL}/generate-proof",
        json={"user_lat": user_lat, "user_long": user_long, "gym_id": gym_id},
    )

    assert response.status_code == 200
    proof_data = response.json()
    assert proof_data["success"] == True
    assert "proof" in proof_data
    assert "public_inputs" in proof_data

    print("✅ Successfully generated ZK proof")
    return proof_data


def test_contract_checkin(proof_data, gym_id=1):
    """Testar check-in no contrato usando a prova gerada"""
    try:
        # Converter inputs públicos para inteiros
        public_inputs = [int(input_val) for input_val in proof_data["public_inputs"]]

        # Preparar dados da transação
        proof_bytes = bytes.fromhex(proof_data["proof"].replace("0x", ""))

        # Construir transação
        txn = contract.functions.checkin(
            gym_id, proof_bytes, public_inputs
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

        # Esperar pela confirmação
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        assert receipt.status == 1, "Transaction failed"
        print(f"✅ Check-in transaction successful: {receipt.transactionHash.hex()}")

        # Verificar check-in no contrato
        checkin_count = contract.functions.getUserGymCheckins(
            account.address, gym_id
        ).call()
        print(f"✅ User now has {checkin_count} check-ins at gym {gym_id}")

        return receipt

    except Exception as e:
        print(f"❌ Error during contract check-in: {str(e)}")
        raise


def run_integration_test():
    """Executar teste de integração completo"""
    print("🔍 Starting integration test...")

    test_api_health()
    gyms = test_get_gyms()

    # Escolher a primeira academia para o teste
    gym_id = gyms[0]["id"]
    print(f"🏋️ Testing with gym: {gyms[0]['name']} (ID: {gym_id})")

    proof_data = test_generate_proof(gym_id)
    receipt = test_contract_checkin(proof_data, gym_id)

    print("✨ Integration test completed successfully!")


if __name__ == "__main__":
    run_integration_test()
