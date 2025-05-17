// Circuito para verificar se o usuário está dentro do perímetro da academia
fn main(
    // Coordenadas do usuário (multiplicadas por 10^6 para precisão)
    user_lat: Field,
    user_long: Field,
    
    // Coordenadas da academia
    gym_lat: Field,
    gym_long: Field,
    
    // Distância máxima permitida (ao quadrado)
    max_distance_squared: Field
) {
    // Calcular diferença em coordenadas
    let lat_diff = if user_lat > gym_lat { 
        user_lat - gym_lat 
    } else { 
        gym_lat - user_lat 
    };
    
    let long_diff = if user_long > gym_long { 
        user_long - gym_long 
    } else { 
        gym_long - user_long 
    };
    
    // Versão simplificada do cálculo de distância (distância euclidiana ao quadrado)
    let distance_squared = lat_diff * lat_diff + long_diff * long_diff;
    
    // Verificar se o usuário está perto o suficiente
    constrain distance_squared <= max_distance_squared;
} 