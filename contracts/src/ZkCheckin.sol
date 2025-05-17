// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/INoirVerifier.sol";

contract ZkCheckin is Ownable {
    INoirVerifier public verifier;

    struct Gym {
        uint256 lat; // Latitude * 10^6 (positive number)
        uint256 long; // Longitude * 10^6 + 180*10^6 (shifted to make negative values positive)
        uint256 maxDistanceSquared;
        bool active;
    }

    mapping(uint256 => Gym) public gyms;
    mapping(address => uint256) public lastCheckin;
    mapping(address => mapping(uint256 => uint256)) public userGymCheckins;

    event GymRegistered(
        uint256 indexed gymId,
        uint256 lat,
        uint256 long,
        uint256 maxDistanceSquared
    );
    event GymUpdated(
        uint256 indexed gymId,
        uint256 lat,
        uint256 long,
        uint256 maxDistanceSquared
    );
    event GymStatusChanged(uint256 indexed gymId, bool active);
    event CheckInCompleted(
        address indexed user,
        uint256 indexed gymId,
        uint256 timestamp
    );

    constructor(address _verifierAddress) Ownable(msg.sender) {
        verifier = INoirVerifier(_verifierAddress);
    }

    function registerGym(
        uint256 gymId,
        uint256 lat,
        uint256 long,
        uint256 maxDistanceMeters
    ) external onlyOwner {
        require(
            gyms[gymId].active == false,
            "Gym already registered and active"
        );

        uint256 maxDistanceSquared = maxDistanceMeters * maxDistanceMeters * 10;

        gyms[gymId] = Gym(lat, long, maxDistanceSquared, true);

        emit GymRegistered(gymId, lat, long, maxDistanceSquared);
    }

    function updateGym(
        uint256 gymId,
        uint256 lat,
        uint256 long,
        uint256 maxDistanceMeters
    ) external onlyOwner {
        require(gyms[gymId].active, "Gym not active");

        uint256 maxDistanceSquared = maxDistanceMeters * maxDistanceMeters * 10;

        gyms[gymId].lat = lat;
        gyms[gymId].long = long;
        gyms[gymId].maxDistanceSquared = maxDistanceSquared;

        emit GymUpdated(gymId, lat, long, maxDistanceSquared);
    }

    function setGymStatus(uint256 gymId, bool active) external onlyOwner {
        require(gyms[gymId].lat > 0, "Gym does not exist");
        gyms[gymId].active = active;
        emit GymStatusChanged(gymId, active);
    }

    function checkin(
        uint256 gymId,
        bytes calldata zkProof,
        uint256[] calldata publicInputs
    ) external {
        require(gyms[gymId].active, "Gym not active");
        require(verifier.verify(zkProof, publicInputs), "Invalid ZK proof");

        require(publicInputs[1] == gyms[gymId].lat, "Gym latitude mismatch");
        require(publicInputs[2] == gyms[gymId].long, "Gym longitude mismatch");
        require(
            publicInputs[3] <= gyms[gymId].maxDistanceSquared,
            "Distance constraint mismatch"
        );

        lastCheckin[msg.sender] = block.timestamp;
        userGymCheckins[msg.sender][gymId]++;

        emit CheckInCompleted(msg.sender, gymId, block.timestamp);
    }

    function getUserGymCheckins(
        address user,
        uint256 gymId
    ) external view returns (uint256) {
        return userGymCheckins[user][gymId];
    }

    function hasRecentCheckin(address user) external view returns (bool) {
        return (block.timestamp - lastCheckin[user]) < 1 days;
    }

    function setVerifier(address _verifierAddress) external onlyOwner {
        verifier = INoirVerifier(_verifierAddress);
    }
}
