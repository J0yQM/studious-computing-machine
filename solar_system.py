import sys
import math
# from turtle import Screen # This will be addressed in a later step
import pygame

#---------------- Congiguration ----------------#
WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
FPS = 60

#  Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0) #Sun
BLUE = (0, 0, 255) #Earth
RED = (255, 0, 0) #Mars
GRAY = (200, 200, 200) #Orbit color
ORANGE = (255, 165, 0) #Mercury
BROWN = (165, 42, 42) #Venus

# Planet data: (name, color, orbital_radius_px, size_px, orbital_period_seconds)
PLANETS = [
    ("Mercury", ORANGE, 60, 4, 10),
    ("Venus", BROWN, 90, 6, 20),
    ("Earth", BLUE, 120, 8, 30),
    ("Mars", RED, 160, 6, 40),
]

#Particle settings
PARTICLE_COLOR = WHITE
PARTICLE_RADIUS = 5
PARTICLE_SPEED = 200 # in pixels per second

#---------------- Helper Functions ----------------#
def polar_to_cartesian(radius, angle):
    """Convert polar coordinates to cartesian."""
    x = radius * math.cos(angle)  # x-coordinate in Cartesian space
    y = radius * math.sin(angle)  # y-coordinate in Cartesian space
    return x, y  # Returns the Cartesian coordinates (x, y) as a tuple

#---------------- Main Program----------------#
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # <- Define "screen" here
    pygame.display.set_caption("Solar System Particle Simulation")
    clock = pygame.time.Clock()

    #Initialize time counter (in seconds)
    elapsed_time = 0.0

    # Inital particle position: start just outside Earth's orbit, at angle 0
    particle_x = CENTER[0] + PLANETS[2][2] + PARTICLE_RADIUS
    particle_y = CENTER[1]
    particle_pos = pygame.math.Vector2(particle_x, particle_y)
    velocity = pygame.math.Vector2(0, 0)

    running = True
    while running:
        dt = clock.tick(FPS)/1000.0  # Convert milliseconds to seconds
        elapsed_time += dt

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #particle movement
        keys = pygame.key.get_pressed()
        velocity.x = 0
        velocity.y = 0
        if keys[pygame.K_LEFT]:
            velocity.x -= PARTICLE_SPEED
        if keys[pygame.K_RIGHT]:
            velocity.x += PARTICLE_SPEED
        if keys[pygame.K_UP]:
            velocity.y -= PARTICLE_SPEED
        if keys[pygame.K_DOWN]:
            velocity.y += PARTICLE_SPEED

        #Normalize diagonal movement so speed is constant
    if velocity.length_squared() > 0:
        velocity = velocity.normalize() * PARTICLE_SPEED

    # Normalize diagonal movement so speed is constant
    particle_pos += velocity * dt
    #Boundary check: keep particle inside window
    particle_pos.x = max(PARTICLE_RADIUS, min(WIDTH - PARTICLE_RADIUS, particle_pos.x))
    particle_pos.y = max(PARTICLE_RADIUS, min(HEIGHT - PARTICLE_RADIUS, particle_pos.y))

    #Drawing
    screen.fill(BLACK)
    #Draw Sun
    pygame.draw.circle(screen, YELLOW, CENTER, 20)

    #Draw orbits and planets
    for name, color, orbit_radius, size, period in PLANETS:
        #Orbit circle
        pygame.draw.circle(screen, GRAY, CENTER, orbit_radius, 1)

        #compute planet angle (radians) from elapsed time
        #Complete one orbit in 'period' seconds -> angular velocity = 2 * pi / period
        angle = (2 * math.pi * elapsed_time) / period
        pos = polar_to_cartesian(orbit_radius, angle)
        pygame.draw.circle(screen, color, (int(CENTER[0] + pos[0]), int(CENTER[1] + pos[1])), size)
    pygame.draw.circle(screen, PARTICLE_COLOR, (int(particle_pos.x), int(particle_pos.y)), PARTICLE_RADIUS)
    #Draw particle
    pygame.draw.circle(screen, PARTICLE_COLOR, (int(particle_pos.x), int(particle_pos.y)), PARTICLE_RADIUS)

    #Update display
    pygame.display.flip()

    # End of main loop
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
