from math import radians, sin, cos

base_angles = [45, 75, 105, 135, -135, -105, -75, -45]
a = 1.5
b = 1.0 
# ^ Ellipse axes for body

# Pre-calculate base position of the legs since it'll be the same each time
base_angles = [radians(angle) for angle in base_angles]
base_positions = []
for angle in base_angles:
    x_base = a * cos(angle)
    y_base = b * sin(angle)
    base_positions.append((x_base, y_base))

def find_endpoints(all_angles: [float]) -> [(float)]:
    """Finds the endpoints of the legs of the spider
    i.e. where the leg connects to the body, its joints, and its end 
    
    Input is 1x24 list of leg angles
    Output is 8x4x3 list of endpoints of leg segments
    8 legs
    4 points (j)
    3 dimensions"""
    endpoints = []
    for i in range(8):
        base_angle = base_angles[i]
        leg_angles = angles[i*3:i*3+3]
        # Initialise empty (apart from known base position)
        leg_endpoints = (
            (base_positions[i][0], base_positions[i][1], 0),
            (0,0,0),
            (0,0,0),
            (0,0,0))
        
        coxa_horizontal_dir = [cos(base_angle) + leg_angles[i],
                               sin(base_angle) + leg_angles[i]]

        

def evaluate_fitness(angles: [float], previous: [float]):
    """Evaluates a spider's fitness based on its joint angles and the previous state"""
    # Plausibility ------------------------------------------------------------

    # Static Plausibility -----------------------

    # Check legs don't intersect body
    # Work out end points of legs
    coxa_endpoints = []

    # No need to check first segment because we know they can't

    # For each leg segment, calculate start and end point


    # Stability ---------------------------------------------------------------


    # Goal-directedness -------------------------------------------------------




def evaluate_population_fitness(population):
    fitnesses = []
    for individual in population:
        return evaluate_fitness(individual)