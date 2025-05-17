// Circuit to verify if user is within gym perimeter
fn main(
    // User coordinates (multiplied by 10^6)
    user_lat: Field,
    user_long: Field,
    // Gym coordinates
    gym_lat: Field,
    gym_long: Field,
    // Maximum allowed distance (squared)
    max_distance_squared: Field,
) {
    // Adjust longitude to match contract system
    let LONG_CONVERSION = 180 * 1_000_000; // 180 degrees * 10^6
    let adjusted_user_long = user_long + LONG_CONVERSION;
    let adjusted_gym_long = gym_long + LONG_CONVERSION;

    // Calculate coordinate differences
    let lat_diff = if (user_lat as u64) > (gym_lat as u64) {
        user_lat - gym_lat
    } else {
        gym_lat - user_lat
    };

    let long_diff = if (adjusted_user_long as u64) > (adjusted_gym_long as u64) {
        adjusted_user_long - adjusted_gym_long
    } else {
        adjusted_gym_long - adjusted_user_long
    };

    // Simplified distance calculation (squared euclidean distance)
    let distance_squared = lat_diff * lat_diff + long_diff * long_diff;

    // Check if user is close enough
    assert((distance_squared as u64) <= (max_distance_squared as u64));
}
