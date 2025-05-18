// Circuit to verify if user is within gym perimeter
#[export]
fn main(
    // User coordinates (private)
    user_lat: Field,
    user_long: Field,
    // Gym coordinates
    gym_lat: Field,
    gym_long: Field,
    // Maximum allowed distance
    max_distance_squared: Field,
) -> pub Field {
    // Calculate coordinate differences (cast to i64 for comparisons)
    let lat_diff = if (user_lat as i64) > (gym_lat as i64) {
        user_lat - gym_lat
    } else {
        gym_lat - user_lat
    };

    let long_diff = if (user_long as i64) > (gym_long as i64) {
        user_long - gym_long
    } else {
        gym_long - user_long
    };

    // Simplified distance calculation (squared euclidean distance)
    let distance_squared = lat_diff * lat_diff + long_diff * long_diff;

    // Check if user is close enough (cast to i64 for comparison)
    assert((distance_squared as u64) <= (max_distance_squared as u64));

    // Retornar os valores publicos
    gym_lat
}
