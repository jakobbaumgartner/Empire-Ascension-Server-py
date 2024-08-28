import math
from perlin_noise import PerlinNoise
from flask import Flask, jsonify, redirect

# Hexagon and grid dimensions
hex_radius = 15
hex_height = hex_radius * math.sqrt(3)
hex_width = hex_radius * 2
grid_width = 250
grid_height = 100

# Terrain types with their respective color codes
terrain_types = {
    'water': '#5B99C2',
    'beach': '#F9DBBA',
    'grass': '#CBE2B5',
    'forest': '#86AB89',
    'mountain': '#A28B55'
}

# Initialize a global variable to store the hexagonal grid
hexagonal_grid = []

# Initialize Perlin noise generator
noise = PerlinNoise(octaves=3, seed=42)

def get_terrain_type(noise_value):
    """Determine the terrain type based on the noise value."""
    if noise_value < -0.3:
        return 'water'
    if noise_value < -0.1:
        return 'beach'
    if noise_value < 0.2:
        return 'grass'
    if noise_value < 0.5:
        return 'forest'
    return 'mountain'

def create_hexagonal_grid():
    """Generate the hexagonal grid and store it in a global variable."""
    global hexagonal_grid
    for row in range(grid_height):
        for col in range(grid_width):
            x = col * hex_width * 0.75
            y = row * hex_height + (col % 2) * (hex_height / 2)
            i = col
            j = row - math.floor(col / 2)
            k = -i - j
            
            noise_value = noise([i * 0.05, j * 0.05])
            terrain = get_terrain_type(noise_value)
            
            hexagon_data = {
                'x': x,
                'y': y,
                'i': i,
                'j': j,
                'k': k,
                'terrain': terrain,
                'color': terrain_types[terrain]
            }
            hexagonal_grid.append(hexagon_data)

# Create the grid once during server initialization
create_hexagonal_grid()

# Flask app initialization
app = Flask(__name__)

@app.route('/')
def index():
    """Redirect to the hex grid."""
    return redirect('/hexgrid')

@app.route('/hexgrid', methods=['GET'])
def get_hex_grid():
    """Return the hexagonal grid as a JSON response."""
    return jsonify(hexagonal_grid)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
