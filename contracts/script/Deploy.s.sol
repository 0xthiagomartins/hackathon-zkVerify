// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Script} from "forge-std/Script.sol";
import "../src/ZkCheckin.sol";
import "../src/mocks/MockVerifier.sol";

contract Deploy is Script {
    // Fator para converter coordenadas negativas em positivas
    uint256 constant LONG_CONVERSION = 180 * 1e6;

    function convertLongitude(int256 long) internal pure returns (uint256) {
        return uint256(long + int256(LONG_CONVERSION));
    }

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        // Deploy do mock do verificador (para testes)
        MockVerifier mockVerifier = new MockVerifier(true);

        // Deploy do contrato principal
        ZkCheckin checkin = new ZkCheckin(address(mockVerifier));

        // Registrar algumas academias para teste
        checkin.registerGym(1, 37423642, convertLongitude(-122084058), 100);
        checkin.registerGym(2, 37422081, convertLongitude(-122084438), 150);

        vm.stopBroadcast();
    }
}
