import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant

# Time step and duration
dt = 60 * 60  # one hour
total_time = 60 * 60 * 24 * 30  # simulate one month
steps = int(total_time / dt)

# Body class
class Body:
    def __init__(self, mass, position, velocity, color='white'):
        self.mass = mass
        self.position = np.array(position, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        self.color = color
        self.path = [self.position.copy()]

    def update(self, force):
        acceleration = force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        self.path.append(self.position.copy())

def compute_gravitational_force(b1, b2):
    distance_vector = b2.position - b1.position
    distance = np.linalg.norm(distance_vector)
    if distance == 0:
        return np.array([0.0, 0.0])
    force_magnitude = G * b1.mass * b2.mass / distance**2
    force_direction = distance_vector / distance
    return force_direction * force_magnitude

# Create bodies
sun = Body(mass=1.989e30, position=[0, 0], velocity=[0, 0], color='yellow')
planet = Body(mass=5.972e24, position=[1.5e11, 0], velocity=[0, 29780], color='blue')  # Earth

bodies = [sun, planet]

# Simulation loop
for _ in range(steps):
    forces = [np.zeros(2) for _ in bodies]
    
    for i, b1 in enumerate(bodies):
        for j, b2 in enumerate(bodies):
            if i != j:
                forces[i] += compute_gravitational_force(b1, b2)
    
    for i, body in enumerate(bodies):
        body.update(forces[i])

# Plotting
fig, ax = plt.subplots()
for body in bodies:
    path = np.array(body.path)
    ax.plot(path[:, 0], path[:, 1], label=f'Mass {body.mass:.2e}', color=body.color)
    ax.plot(path[-1, 0], path[-1, 1], 'o', color=body.color)

ax.set_title('Two-Body Gravitational Simulation')
ax.set_xlabel('X position (m)')
ax.set_ylabel('Y position (m)')
ax.legend()
ax.set_aspect('equal')
plt.show()
