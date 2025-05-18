// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface INoirVerifier {
    function verify(
        uint256[] calldata proof,
        uint256[] calldata publicInputs
    ) external view returns (bool);
}
