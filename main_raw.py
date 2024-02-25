import pygame
import math # sqrt
import sys # exit

# updates per second: 120

# vec2.normalise(self : vec2) -> vec2:
#     dist = math.sqrt(v2.x ** 2 + v2.y ** 2)
#     return v2 / dist
def vec2_normalise(v2 : tuple[float, float]) -> tuple[float, float]:
    dist = math.sqrt(v2[0] ** 2 + v2[1] ** 2)
    return (v2[0] / dist, v2[1] / dist)

# particle.accTowardsRadius(particle : particle, other : particle,
#     other_radius : float, proportion : float) -> None:
#     dif = other.pos - particle.pos
#     self.vel += dif.normalise() * (math.sqrt(dif.x ** 2 + dif.y ** 2) - other_radius) * proportion
def vec2_accTowardsRadius(particle_pos : tuple[float, float], other_pos : tuple[float, float],
        other_radius : float, proportion : float) -> tuple[float, float]:
    dif = (other_pos[0] - particle_pos[0], other_pos[1] - particle_pos[1])
    norm = vec2_normalise(dif)
    f = (math.sqrt(dif[0] ** 2 + dif[1] ** 2) - other_radius) * proportion
    return (norm[0] * f, norm[1] * f)

# physics – links between particles
# reads pos, affects vel
# in a separate function for ease of profiling
def phys_links() -> None:
    for link in links:
        # particles[link.end1_index].accTowardsRadius(
        #     particles[link.end2_index], link.length, phys_coherence)
        # particles[link.end2_index].accTowardsRadius(
        #     particles[link.end1_index], link.length, phys_coherence)
        particle0_pos = particles_pos[link[0]]
        particle1_pos = particles_pos[link[1]]
        t = vec2_accTowardsRadius(particle0_pos, particle1_pos, link[2], phys_coherence)
        particles_vel[link[0]] = (particles_vel[link[0]][0] + t[0],
            particles_vel[link[0]][1] + t[1])
        t = vec2_accTowardsRadius(particle1_pos, particle0_pos, link[2], phys_coherence)
        particles_vel[link[1]] = (particles_vel[link[1]][0] + t[0],
            particles_vel[link[1]][1] + t[1])

# setup – net, and physics constants
net_width, net_height = 20, 20
net_cellSize = 20
net_offsetX, net_offsetY = 40, 50
phys_coherence = 0.4 # 0 to (soft 0.5)
phys_gravity = 0.2
phys_air_resistance = 0.01

# setup – display
disp_size = (1200, 600)
disp_cap = False
disp_active = False

# setup – the net
particles_pos, particles_vel, links = [], [], []
for y in range(net_height):
    for x in range(net_width):
        particles_pos.append((x * net_cellSize + net_offsetX, y * net_cellSize + net_offsetY))
        particles_vel.append((0.0, 0.0))
    for x in range(net_width - 1):
        links.append((y * net_height + x, y * net_height + x + 1, net_cellSize))
        links.append((x * net_width + y, (x + 1) * net_width + y, net_cellSize))

# setup – physics constants, display, and timing
phys_air_resistance = 1 - phys_air_resistance
pygame.init()
disp_pygame = pygame.display.set_mode(disp_size)
disp_font = pygame.font.SysFont("Verdana", 12)
timing_clock = pygame.time.Clock()

# main loop
while True:
    # physics – links between particles (reads pos, affects vel)
    phys_links()

    # physics – gravity, momentum, and air resistance
    # for particle in particles:
    #     particle.vel.y += phys.gravity
    #     particle.pos += particle.vel
    #     particle.vel *= phys.air_resistance
    for index in range(len(particles_pos)):
        particles_vel[index] = (particles_vel[index][0],
            particles_vel[index][1] + phys_gravity)
        particles_pos[index] = (particles_pos[index][0] + particles_vel[index][0],
            particles_pos[index][1] + particles_vel[index][1])
        particles_vel[index] = (particles_vel[index][0] * phys_air_resistance,
            particles_vel[index][1] * phys_air_resistance)

    # physics – pin the top of the net
    for x in range(net_width):
        particles_pos[x] = (x * (net_cellSize * 1.25) + net_offsetX, net_offsetY)

    # rendering – particles and links
    if disp_active:
        for particle_pos in particles_pos: # for particle in particles
            pygame.draw.circle(disp_pygame, (100, 140, 255), particle_pos, 5)
        for link in links:
            pygame.draw.line(disp_pygame, (128, 255, 128),
                particles_pos[link[0]], particles_pos[link[1]], 2)

    # rendering
    screen_text_FPS = int(timing_clock.get_fps())
    screen_text_FPS2 = disp_font.render(
        f"FPS: {screen_text_FPS}", True, (255, 255, 255))
    disp_pygame.blit(screen_text_FPS2, (10, 10))
    pygame.display.flip() # swap buffers
    disp_pygame.fill((0, 0, 0))
    timing_clock.tick(90 if disp_cap else 1000000) # 90 FPS

    # exit test
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit() # pygame.quit()
