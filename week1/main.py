import pygame
import numpy as np
import random

# Configuration

WIDTH = 800
HEIGHT = 800

BOWL_CENTER = np.array([WIDTH / 2, HEIGHT / 2], dtype=float)
BOWL_RADIUS = 300

# Set N number of balls here
NUM_PARTICLES = 25
PARTICLE_RADIUS = 12
PARTICLE_SPEED = 150.0

# Pixels per second squared, +y points DOWN on screen
GRAVITY = np.array([0.0, 900.0])

# Restitution factors (1.0 = elastic, < 1.0 = loss of energy)
WALL_RESTITUTION = 0.9
RESTITUTION = 0.9

FPS = 120

positions = []
velocities = []

for i in range(NUM_PARTICLES):
    # Place particle randomly inside the bowl without overlapping boundary
    angle = random.uniform(0, 2 * np.pi)
    distance = random.uniform(0, BOWL_RADIUS - PARTICLE_RADIUS)

    positions.append(BOWL_CENTER + distance * np.array([
        np.cos(angle),
        np.sin(angle)
    ]))

    # Random initial trajectory
    angle = random.uniform(0, 2 * np.pi)
    velocities.append(PARTICLE_SPEED * np.array([
        np.cos(angle),
        np.sin(angle)
    ]))

# Pygame setup

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulation")
clock = pygame.time.Clock()

running = True

# Main loop

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(FPS) / 1000.0

    ###########################################################################
    # PART 1: GRAVITY, MOVEMENT, AND BOWL WALL COLLISIONS FOR ALL BALLS       #
    ###########################################################################

    for i in range(len(positions)):
        # 1. Update velocity with gravity
        velocities[i] += GRAVITY * dt

        # 2. Update position
        positions[i] += velocities[i] * dt

        # 3. Check wall boundary collision
        to_particle = positions[i] - BOWL_CENTER
        distance = np.linalg.norm(to_particle)

        # Max allowed distance from center to particle center
        max_dist = BOWL_RADIUS - PARTICLE_RADIUS

        if distance > max_dist and distance > 0:
            # Outward normal vector pointing from bowl center to particle
            normal = to_particle / distance

            # Normal velocity component (dot product)
            v_normal = np.dot(velocities[i], normal)

            # Reflect velocity along the normal if heading outward
            if v_normal > 0:
                velocities[i] -= (1 + WALL_RESTITUTION) * v_normal * normal

            # Positional correction: push particle back inside
            positions[i] = BOWL_CENTER + normal * max_dist

    ###########################################################################
    # PART 2: BALL-TO-BALL COLLISIONS                                         #
    ###########################################################################

    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            delta = positions[j] - positions[i]
            dist = np.linalg.norm(delta)

            # Collision condition: distance between centers is less than 2 * radius
            min_dist = 2 * PARTICLE_RADIUS

            if dist < min_dist and dist > 0:
                # Collision normal from ball i to ball j
                normal = delta / dist

                # Relative velocity of ball j with respect to ball i
                rel_velocity = velocities[j] - velocities[i]

                # Velocity component along normal
                vel_along_normal = np.dot(rel_velocity, normal)

                # Process collision only if balls are moving towards each other
                if vel_along_normal < 0:
                    # Impulse scalar for equal-mass elastic/inelastic collision
                    impulse = -(1 + RESTITUTION) * vel_along_normal / 2.0

                    # Apply impulse to velocities
                    velocities[i] -= impulse * normal
                    velocities[j] += impulse * normal

                    # Positional correction to resolve overlap evenly
                    overlap = min_dist - dist
                    separation = normal * (overlap / 2.0)
                    positions[i] -= separation
                    positions[j] += separation

    ###########################################################################
    # Render                                                                  #
    ###########################################################################

    screen.fill((20, 20, 25))

    pygame.draw.circle(
        screen,
        (180, 180, 180),
        BOWL_CENTER.astype(int),
        BOWL_RADIUS,
        width=3
    )

    for position in positions:
        pygame.draw.circle(
            screen,
            (220, 220, 220),
            position.astype(int),
            PARTICLE_RADIUS
        )

    pygame.display.flip()

pygame.quit()