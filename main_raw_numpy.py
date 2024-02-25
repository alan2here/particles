import pygame
import numpy as np
import sys

# updates per second: low

def vec2_normalise(v2):
    dist = np.linalg.norm(v2)
    return v2 / dist if dist != 0 else v2

def vec2_accTowardsRadius(particle_pos, other_pos, other_radius, proportion):
    dif = other_pos - particle_pos
    norm_dif = np.linalg.norm(dif)
    return (dif / norm_dif if norm_dif != 0 else dif) * (norm_dif - other_radius) * proportion

# setup – net, physics constants, and display
net_width, net_height = 20, 20
net_cellSize = 20
net_offsetX, net_offsetY = 40, 50
phys_coherence = 0.4
phys_gravity = 0.2
phys_air_resistance = 0.01
phys_dtype_particle_pos = np.float32
phys_dtype_particle_vel = np.float16
disp_size = (1200, 600)

# setup – the net
particles_pos = np.array([(x * net_cellSize + net_offsetX, y * net_cellSize + net_offsetY)
    for y in range(net_height) for x in range(net_width)], dtype = phys_dtype_particle_pos)
particles_vel = np.zeros((net_width * net_height, 2), dtype = phys_dtype_particle_vel)
links = np.array([(y * net_width + x, y * net_width + x + 1, net_cellSize)
    for y in range(net_height) for x in range(net_width - 1)] +
    [(x * net_width + y, (x + 1) * net_width + y, net_cellSize)
    for x in range(net_width - 1) for y in range(net_height)], dtype = np.uint16)

# setup – physics constants, display, and timing
phys_air_resistance = 1 - phys_air_resistance
pygame.init()
disp_pygame = pygame.display.set_mode(disp_size)
disp_font = pygame.font.SysFont("Verdana", 12)
timing_clock = pygame.time.Clock()

# main loop
while True:
    # physics – links between particles (reads pos, affects vel)
    for link in links:
        particle0_pos = particles_pos[link[0]]
        particle1_pos = particles_pos[link[1]]
        particles_vel[link[0]] += vec2_accTowardsRadius(
            particle0_pos, particle1_pos, link[2], phys_coherence)
        particles_vel[link[1]] += vec2_accTowardsRadius(
            particle1_pos, particle0_pos, link[2], phys_coherence)

    # physics – gravity, momentum, and air resistance
    particles_vel[:, 1] += phys_gravity
    particles_pos += particles_vel
    particles_vel *= phys_air_resistance

    # physics – pin the top of the net
    particles_pos[:net_width, 1] = net_offsetY
    particles_pos[:net_width, 0] = np.linspace(net_offsetX, net_offsetX +
        net_cellSize * (net_width - 1) * 1.25, net_width)

    # rendering – the net
    for particle_pos in particles_pos:
        pygame.draw.circle(disp_pygame, (100, 140, 255), particle_pos.astype(int), 5)
    for link in links:
        pygame.draw.line(disp_pygame, (128, 255, 128),
            particles_pos[link[0]].astype(int), particles_pos[link[1]].astype(int), 2)

    # rendering
    screen_text_FPS = int(timing_clock.get_fps())
    screen_text_FPS2 = disp_font.render(
        f"FPS: {screen_text_FPS}",
        True, (255, 255, 255))
    disp_pygame.blit(screen_text_FPS2, (10, 10))
    pygame.display.flip()
    disp_pygame.fill((0, 0, 0))
    timing_clock.tick(90)

    # exit test
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
