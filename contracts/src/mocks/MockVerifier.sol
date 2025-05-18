// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../interfaces/INoirVerifier.sol";

contract MockVerifier is INoirVerifier {
    bool private shouldPass;

    constructor(bool _shouldPass) {
        shouldPass = _shouldPass;
    }

    function verify(
        bytes calldata,
        uint256[] calldata
    ) external view override returns (bool) {
        return shouldPass;
    }

    function setShouldPass(bool _shouldPass) external {
        shouldPass = _shouldPass;
    }
}
