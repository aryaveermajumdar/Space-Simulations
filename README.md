# Space-Simulations
Hello There!
While this code has been written for the purpose of tutoring the OIS Physics Team, feel free to use copies of this code!
Here's the cleaned-up text as normal, readable content:

Single-Planet RK4 Orbit Simulator

This is a Python simulation of a planet orbiting a central star (like the Sun) using the Runge-Kutta 4th order (RK4) numerical integration method. It visualizes orbital motion in 2D using Pygame.

Features:

 - Simulates a single planet orbiting a central mass (e.g., Sun).
 - Uses RK4 integration for high accuracy in orbital calculations.
 - Allows the user to input: initial distance from the Sun (AU), tangential velocity (km/s), radial velocity (km/s).
 - Continuous visualization of the orbit with a trailing path.
 - User can quit at any time by pressing Q or closing the window.

Requirements:
 - Python 3.8 or higher
 - Pygame library (pip install pygame)

How to Run:
 - Clone or download the repository.
 - Run the Python script: python single_planet_rk4.py
 - Follow the terminal prompts to input initial parameters or press Enter/d for defaults.
 - Watch the planet orbit and interact using the Pygame window.

Default Example:
 - Distance: 1 AU
 - Tangential velocity: 24 km/s
 - Radial velocity: 0 km/s
This produces a nearly circular orbit similar to Earth's.

Notes:
 - The simulation uses a fixed scale (meters → pixels) for visualization.
 - Adjust DT (time step) for faster/slower simulation and higher accuracy.
 - Suitable for educational purposes and experimenting with orbital mechanics.

—————————————————————

README for N-Body RK4 Orbit Simulator

This Python program simulates the motion of multiple bodies under mutual gravitational forces using the Runge-Kutta 4th order (RK4) numerical method. Visualized in 2D using Pygame, it allows experimentation with realistic orbital dynamics.

Features:
 - Simulates any number of bodies, including planets, moons, and stars.
 - Each body's gravity affects every other body (full N-body interaction).
 - User input for: mass (kg), distance from origin (AU), angle (degrees), tangential speed (km/s).
 - Includes a DEFAULT preset with a Sun and two massive planets.
 - Trails visualize the path of each body.
 - Continuous simulation until the user presses Q or closes the window.

Requirements:
 - Python 3.8 or higher
 - Pygame library (pip install pygame)

How to Run:
 - Clone or download the repository.
 - Run the Python script: python n_body_rk4.py
 - Input the number of bodies or type DEFAULT to use the preset system.
 - Enter mass, distance, angle, and tangential speed for each body (or type d for default).
 - Watch the simulation in real-time.

Default Preset (3 Bodies):
 - Body 0 (Sun): mass = 1.989e30 kg, distance = 0 AU, speed = 0 km/s
 - Body 1: mass = 5e26 kg, distance = 1 AU, speed = 29.78 km/s
 - Body 2: mass = 5e26 kg, distance = 1.2 AU at 45°, speed = 27 km/s
This creates visible orbital interactions between two heavy planets and the Sun.

Notes:
 - Trails are limited to avoid excessive memory use (max 3000 points).
 - Time step (tick) can be adjusted for speed/accuracy trade-off.

meters_to_pixels_ratio controls the zoom level of the visualization.

Suitable for exploring orbital mechanics, planet interactions, and educational demonstrations of N-body physics.
