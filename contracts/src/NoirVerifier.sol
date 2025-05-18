// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./interfaces/INoirVerifier.sol";
import "./plonk/UltraPlonk.sol";

contract NoirVerifier is INoirVerifier, UltraPlonk {
    // Constantes para o verificador
    uint256 constant NUM_PUBLIC_INPUTS = 4; // gym_id, gym_lat, gym_long, max_distance_squared

    constructor() {
        // Inicializar verifyingKey com os parâmetros gerados pelo Noir
        // TODO: Adicionar parâmetros reais
    }

    function verify(
        bytes calldata _proof,
        uint256[] calldata publicInputs
    ) public view override returns (bool) {
        require(
            publicInputs.length == NUM_PUBLIC_INPUTS,
            "Invalid number of public inputs"
        );

        // Decodificar a prova
        Proof memory proof = decodeProof(_proof);

        // Verificar a prova usando UltraPlonk
        return verifyProof(proof, publicInputs);
    }

    function decodeProof(
        bytes calldata _proof
    ) internal pure returns (Proof memory) {
        // TODO: Decodificar bytes da prova para a estrutura Proof
    }

    function verifyProof(
        Proof memory proof,
        uint256[] calldata publicInputs
    ) internal view returns (bool) {
        // TODO: Implementar verificação usando UltraPlonk
    }
}
