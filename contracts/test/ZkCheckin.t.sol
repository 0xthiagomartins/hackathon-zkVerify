// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Test} from "forge-std/Test.sol";
import "../src/ZkCheckin.sol";
import "../src/mocks/MockVerifier.sol";

contract ZkCheckinTest is Test {
    ZkCheckin public checkin;
    MockVerifier public mockVerifier;

    address constant OWNER = address(0x1);
    address constant USER = address(0x2);

    uint256 constant GYM_ID = 1;
    uint256 constant LAT = 37423642;
    uint256 constant LONG_CONVERSION = 180 * 1e6;
    uint256 constant LONG = LONG_CONVERSION - 122084058; // Converting negative to positive
    uint256 constant MAX_DISTANCE = 100;

    function setUp() public {
        vm.startPrank(OWNER);
        mockVerifier = new MockVerifier(true);
        checkin = new ZkCheckin(address(mockVerifier));
        checkin.registerGym(GYM_ID, LAT, LONG, MAX_DISTANCE);
        vm.stopPrank();
    }

    function testRegisterGym() public {
        vm.startPrank(OWNER);
        uint256 newGymId = 2;
        checkin.registerGym(
            newGymId,
            LAT + 1000,
            LONG - 1000,
            MAX_DISTANCE * 2
        );

        (
            uint256 lat,
            uint256 long,
            uint256 maxDistanceSquared,
            bool active
        ) = checkin.gyms(newGymId);

        assertEq(lat, LAT + 1000);
        assertEq(long, LONG - 1000);
        assertEq(
            maxDistanceSquared,
            (MAX_DISTANCE * 2) * (MAX_DISTANCE * 2) * 10
        );
        assertTrue(active);
        vm.stopPrank();
    }

    function testUpdateGym() public {
        vm.startPrank(OWNER);
        uint256 newLat = LAT + 2000;
        uint256 newLong = LONG - 2000;
        uint256 newMaxDistance = MAX_DISTANCE * 3;

        checkin.updateGym(GYM_ID, newLat, newLong, newMaxDistance);

        (uint256 lat, uint256 long, uint256 maxDistanceSquared, ) = checkin
            .gyms(GYM_ID);

        assertEq(lat, newLat);
        assertEq(long, newLong);
        assertEq(maxDistanceSquared, newMaxDistance * newMaxDistance * 10);
        vm.stopPrank();
    }

    function testSetGymStatus() public {
        vm.startPrank(OWNER);
        checkin.setGymStatus(GYM_ID, false);

        (, , , bool active) = checkin.gyms(GYM_ID);
        assertFalse(active);

        checkin.setGymStatus(GYM_ID, true);

        (, , , active) = checkin.gyms(GYM_ID);
        assertTrue(active);
        vm.stopPrank();
    }

    function testCheckin() public {
        vm.startPrank(USER);

        uint256[] memory publicInputs = new uint256[](4);
        publicInputs[0] = 37423640; // user_lat
        publicInputs[1] = LAT; // gym_lat
        publicInputs[2] = LONG; // gym_long
        publicInputs[3] = 900; // max_distance_squared

        checkin.checkin(GYM_ID, bytes("dummy_proof"), publicInputs);

        assertEq(checkin.userGymCheckins(USER, GYM_ID), 1);
        assertTrue(checkin.lastCheckin(USER) > 0);
        vm.stopPrank();
    }

    function test_RevertWhen_GymInactive() public {
        vm.prank(OWNER);
        checkin.setGymStatus(GYM_ID, false);

        vm.startPrank(USER);
        uint256[] memory publicInputs = new uint256[](4);

        vm.expectRevert("Gym not active");
        checkin.checkin(GYM_ID, bytes("dummy_proof"), publicInputs);
        vm.stopPrank();
    }

    function test_RevertWhen_InvalidProof() public {
        MockVerifier(address(mockVerifier)).setShouldPass(false);

        vm.startPrank(USER);
        uint256[] memory publicInputs = new uint256[](4);
        publicInputs[0] = 37423640;
        publicInputs[1] = LAT;
        publicInputs[2] = LONG;
        publicInputs[3] = 900;

        vm.expectRevert("Invalid ZK proof");
        checkin.checkin(GYM_ID, bytes("invalid_proof"), publicInputs);
        vm.stopPrank();
    }
}
