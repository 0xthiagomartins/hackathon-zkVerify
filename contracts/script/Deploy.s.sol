// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Script} from "forge-std/Script.sol";
import {ZkCheckin} from "../src/ZkCheckin.sol";
import {NoirVerifier} from "../src/NoirVerifier.sol";

contract DeployScript is Script {
    // Fator para converter coordenadas negativas em positivas
    uint256 constant LONG_CONVERSION = 180 * 1e6;

    function convertLongitude(int256 long) internal pure returns (uint256) {
        return uint256(long + int256(LONG_CONVERSION));
    }

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");

        vm.startBroadcast(deployerPrivateKey);

        // Deploy do verificador
        NoirVerifier verifier = new NoirVerifier();

        // Deploy do contrato principal usando o endereço do verificador
        ZkCheckin zkCheckin = new ZkCheckin(address(verifier));

        // Registrar algumas academias para teste
        zkCheckin.registerGym(1, 37423642, convertLongitude(-122084058), 100);
        zkCheckin.registerGym(2, 37422081, convertLongitude(-122084438), 150);

        vm.stopBroadcast();
    }
}
