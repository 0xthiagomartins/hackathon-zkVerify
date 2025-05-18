// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/INoirVerifier.sol";

contract ZkCheckin is Ownable {
    struct Gym {
        uint256 id;
        uint256 lat;
        uint256 long;
        uint256 maxDistanceSquared;
        bool active;
    }

    // Mapping de academias registradas
    mapping(uint256 => Gym) public gyms;
    // Mapping de check-ins por usuário e academia
    mapping(address => mapping(uint256 => uint256)) public lastCheckin;
    // Verificador de provas ZK
    INoirVerifier public verifier;

    event GymRegistered(uint256 indexed gymId, uint256 lat, uint256 long);
    event CheckinRegistered(
        address indexed user,
        uint256 indexed gymId,
        uint256 timestamp
    );

    constructor(address _verifierAddress) Ownable(msg.sender) {
        verifier = INoirVerifier(_verifierAddress);
    }

    function registerGym(
        uint256 _id,
        uint256 _lat,
        uint256 _long,
        uint256 _maxDistanceSquared
    ) external onlyOwner {
        require(!gyms[_id].active, "Gym already registered");

        gyms[_id] = Gym({
            id: _id,
            lat: _lat,
            long: _long,
            maxDistanceSquared: _maxDistanceSquared,
            active: true
        });

        emit GymRegistered(_id, _lat, _long);
    }

    function checkin(
        uint256 _gymId,
        uint256[] calldata _proof,
        uint256[] calldata _publicInputs
    ) external {
        require(gyms[_gymId].active, "Gym not registered");

        // Verificar a prova ZK
        require(verifier.verify(_proof, _publicInputs), "Invalid proof");

        // Registrar check-in
        lastCheckin[msg.sender][_gymId] = block.timestamp;

        emit CheckinRegistered(msg.sender, _gymId, block.timestamp);
    }

    function getLastCheckin(
        address _user,
        uint256 _gymId
    ) external view returns (uint256) {
        return lastCheckin[_user][_gymId];
    }

    function updateVerifier(address _newVerifier) external onlyOwner {
        verifier = INoirVerifier(_newVerifier);
    }
}
