mod test {
    use dep::std;

    #[test]
    fn test_within_range() {
        // Test coordinates (multiplied by 10^6)
        let user_lat = 37423640;
        let user_long = -122084050;
        let gym_lat = 37423642;
        let gym_long = -122084058;
        let max_distance_squared = 1000;

        // Should pass as it's within perimeter
        main(user_lat, user_long, gym_lat, gym_long, max_distance_squared);
    }

    #[test(should_fail)]
    fn test_outside_range() {
        // Test coordinates far apart
        let user_lat = 37423640;
        let user_long = -122084050;
        let gym_lat = 37423642;
        let gym_long = -122084058;
        let max_distance_squared = 10; // Too small to pass

        // Should fail as it's outside perimeter
        main(user_lat, user_long, gym_lat, gym_long, max_distance_squared);
    }
}
