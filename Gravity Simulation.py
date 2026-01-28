import pygame
import math

gravitational_constant = 6.674e-11
time_step_seconds = 70000

window_width = 900
window_height = 700
window_center_x = window_width // 2
window_center_y = window_height // 2

meters_to_pixels_ratio = 1e9

pygame.init()
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("n-Body RK4 Simulation")
frame_controller = pygame.time.Clock()

def get_numeric_input(prompt_message, fallback_value):
    raw_value = input(f"{prompt_message} [default = {fallback_value}, type 'd' for default]: ").strip()
    if raw_value.lower() == 'd' or raw_value == '':
        return fallback_value
    try:
        return float(raw_value)
    except ValueError:
        print("Invalid input, using default.")
        return fallback_value

def compute_net_acceleration(index, positions_x, positions_y, masses):
    accel_x = 0.0
    accel_y = 0.0
    for other_index in range(len(positions_x)):
        if index == other_index:
            continue
        delta_x = positions_x[other_index] - positions_x[index]
        delta_y = positions_y[other_index] - positions_y[index]
        distance_squared = delta_x*delta_x + delta_y*delta_y
        if distance_squared == 0:
            continue
        distance = math.sqrt(distance_squared)
        factor = gravitational_constant * masses[other_index] / (distance**3)
        accel_x += factor * delta_x
        accel_y += factor * delta_y
    return accel_x, accel_y

def rk4_integrator_step(positions_x, positions_y, velocities_x, velocities_y, masses, delta_time):
    total_bodies = len(positions_x)
    accel1_x = [0]*total_bodies
    accel1_y = [0]*total_bodies
    for i in range(total_bodies):
        accel1_x[i], accel1_y[i] = compute_net_acceleration(i, positions_x, positions_y, masses)

    temp_x2 = [positions_x[i] + velocities_x[i]*delta_time/2 for i in range(total_bodies)]
    temp_y2 = [positions_y[i] + velocities_y[i]*delta_time/2 for i in range(total_bodies)]
    temp_vx2 = [velocities_x[i] + accel1_x[i]*delta_time/2 for i in range(total_bodies)]
    temp_vy2 = [velocities_y[i] + accel1_y[i]*delta_time/2 for i in range(total_bodies)]
    accel2_x = [0]*total_bodies
    accel2_y = [0]*total_bodies
    for i in range(total_bodies):
        accel2_x[i], accel2_y[i] = compute_net_acceleration(i, temp_x2, temp_y2, masses)

    temp_x3 = [positions_x[i] + temp_vx2[i]*delta_time/2 for i in range(total_bodies)]
    temp_y3 = [positions_y[i] + temp_vy2[i]*delta_time/2 for i in range(total_bodies)]
    temp_vx3 = [velocities_x[i] + accel2_x[i]*delta_time/2 for i in range(total_bodies)]
    temp_vy3 = [velocities_y[i] + accel2_y[i]*delta_time/2 for i in range(total_bodies)]
    accel3_x = [0]*total_bodies
    accel3_y = [0]*total_bodies
    for i in range(total_bodies):
        accel3_x[i], accel3_y[i] = compute_net_acceleration(i, temp_x3, temp_y3, masses)

    temp_x4 = [positions_x[i] + temp_vx3[i]*delta_time for i in range(total_bodies)]
    temp_y4 = [positions_y[i] + temp_vy3[i]*delta_time for i in range(total_bodies)]
    temp_vx4 = [velocities_x[i] + accel3_x[i]*delta_time for i in range(total_bodies)]
    temp_vy4 = [velocities_y[i] + accel3_y[i]*delta_time for i in range(total_bodies)]
    accel4_x = [0]*total_bodies
    accel4_y = [0]*total_bodies
    for i in range(total_bodies):
        accel4_x[i], accel4_y[i] = compute_net_acceleration(i, temp_x4, temp_y4, masses)

    for i in range(total_bodies):
        positions_x[i] += delta_time*(velocities_x[i] + 2*temp_vx2[i] + 2*temp_vx3[i] + temp_vx4[i]) / 6
        positions_y[i] += delta_time*(velocities_y[i] + 2*temp_vy2[i] + 2*temp_vy3[i] + temp_vy4[i]) / 6
        velocities_x[i] += delta_time*(accel1_x[i] + 2*accel2_x[i] + 2*accel3_x[i] + accel4_x[i]) / 6
        velocities_y[i] += delta_time*(accel1_y[i] + 2*accel2_y[i] + 2*accel3_y[i] + accel4_y[i]) / 6
    return positions_x, positions_y, velocities_x, velocities_y

print(" ")
print("SETUP")
user_setup_input = input("Number of bodies: ").strip() # [default=3, type 'd' for default, or type 'DEFAULT' for preset system]

positions_x = []
positions_y = []
velocities_x = []
velocities_y = []
masses = []
orbit_trails = []

if user_setup_input.lower() == 'default':
    positions_x = [0.0, 1.0 * 1.496e11, 1.2 * 1.496e11 * math.cos(math.radians(45))]
    positions_y = [0.0, 0.0, 1.2 * 1.496e11 * math.sin(math.radians(45))]
    velocities_x = [0.0, 0.0, -27e3 * math.sin(math.radians(45))]
    velocities_y = [0.0, 29.78e3, 27e3 * math.cos(math.radians(45))]
    masses = [1.989e30, 5e26, 5e26]
    orbit_trails = [[] for _ in range(3)]
    total_bodies = 3
else:
    total_bodies = int(get_numeric_input("Number of bodies", 3))
    for body_index in range(total_bodies):
        print(f"\nBody {body_index}")
        body_mass = get_numeric_input("mass (kg)", 1.0e24)
        body_distance = get_numeric_input("distance from origin (AU)", 0.0) * 1.496e11
        body_angle = get_numeric_input("angle (deg)", 0.0) * math.pi / 180
        body_tangential_speed = get_numeric_input("tangential speed (kms-1)", 0.0) * 1e3
        positions_x.append(body_distance * math.cos(body_angle))
        positions_y.append(body_distance * math.sin(body_angle))
        velocities_x.append(-body_tangential_speed * math.sin(body_angle))
        velocities_y.append(body_tangential_speed * math.cos(body_angle))
        masses.append(body_mass)
        orbit_trails.append([])

simulation_running = True

while simulation_running:
    frame_controller.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simulation_running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            simulation_running = False

    positions_x, positions_y, velocities_x, velocities_y = rk4_integrator_step(
        positions_x, positions_y, velocities_x, velocities_y, masses, time_step_seconds
    )

    display_surface.fill((0, 0, 0))

    for i in range(total_bodies):
        orbit_trails[i].append((positions_x[i], positions_y[i]))
        if len(orbit_trails[i]) > 3000:
            orbit_trails[i].pop(0)
        trail_path = [
            (window_center_x + int(px / meters_to_pixels_ratio),
             window_center_y + int(py / meters_to_pixels_ratio))
            for px, py in orbit_trails[i]
        ]
        if len(trail_path) > 1:
            pygame.draw.lines(display_surface, (120, 120, 120), False, trail_path, 1)
        pygame.draw.circle(
            display_surface,
            (200, 200 - i*20 % 200, 255),
            (window_center_x + int(positions_x[i]/meters_to_pixels_ratio),
             window_center_y + int(positions_y[i]/meters_to_pixels_ratio)),
            max(3, int(math.log10(masses[i]) - 20))
        )

    pygame.display.flip()

pygame.quit()
