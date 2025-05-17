#[test]
fn test_within_range() {
    // User inside gym range
    let user_lat = 37423640;
    let user_long = -122084050;
    let gym_lat = 37423642;
    let gym_long = -122084058;
    let max_distance_squared = 1000;

    // Should pass
    main(user_lat, user_long, gym_lat, gym_long, max_distance_squared);
}

#[test(should_fail)]
fn test_outside_range() {
    // User far from gym
    let user_lat = 37423640;
    let user_long = -122084050;
    let gym_lat = 37423642;
    let gym_long = -122084058;
    let max_distance_squared = 10; // Muito próximo para passar

    // Should fail
    main(user_lat, user_long, gym_lat, gym_long, max_distance_squared);
} 