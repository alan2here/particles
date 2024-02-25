import pygame
from nice_stuff import vec2
import math # sqrt
import sys # exit

# updates per second: 50

class particle: pass

class particle:
    def __init__(self, pos : vec2):
        self.pos = pos
        self.vel = vec2(0, 0)

    def accTowardsRadius(self : particle, other : particle,
            other_radius : float, proportion : float) -> None:
        dif = other.pos - self.pos
        self.vel += dif.normalise() * (math.sqrt(dif.x ** 2 + dif.y ** 2) - other_radius) * proportion

class link:
    def __init__(self, end1_index : int, end2_index : int, length : float):
        self.end1_index = end1_index
        self.end2_index = end2_index
        self.length = length

class net:
    # the net contains particles and links between them
    # in this example they are arranged in a grid
    width, height = 20, 20
    cellSize = 20
    offsetX, offsetY = 40, 50

# setup – the net
particles, links = [], []
for y in range(net.height):
    for x in range(net.width):
        particles += [particle(vec2(x * net.cellSize + net.offsetX, y * net.cellSize + net.offsetY))]
    for x in range(net.width - 1):
        links += [link(y * net.height + x, y * net.height + x + 1, net.cellSize)]
        links += [link(x * net.width + y, (x + 1) * net.width + y, net.cellSize)]

# ---

# setup – physics constants, display, and timing

class phys:
    coherence = 0.4 # 0 to (soft 0.5)
    gravity = 0.2
    air_resistance = 0.01

    def init():
        phys.air_resistance = 1 - phys.air_resistance

    # physics – links between particles
    # reads pos, affects vel
    # in a separate function for ease of profiling
    def links() -> None:
        for link in links:
            particles[link.end1_index].accTowardsRadius(
                particles[link.end2_index], link.length, phys.coherence)
            particles[link.end2_index].accTowardsRadius(
                particles[link.end1_index], link.length, phys.coherence)

class disp:
    size = (1200, 600)
    cap = False
    active = False

    def init():
        disp.pygame = pygame.display.set_mode(disp.size)
        disp.font = pygame.font.SysFont("Verdana", 12)

phys.init()
pygame.init()
disp.init()
timing_clock = pygame.time.Clock()

# ---

# main loop
while True:
    # physics – links between particles (reads pos, affects vel)
    phys.links() # in a separate function for ease of profiling

    # physics – gravity, momentum, and air resistance
    for particle in particles:
        particle.vel.y += phys.gravity
        particle.pos += particle.vel
        particle.vel *= phys.air_resistance

    # physics – pin the top of the net
    for x in range(net.width):
        particles[x].pos = vec2(x * (net.cellSize * 1.25) + net.offsetX, net.offsetY)

    # rendering – the net
    if disp.active:
        for point in particles:
            pygame.draw.circle(disp.pygame, (100, 140, 255), (point.pos.x, point.pos.y), 5)
        for link in links:
            pygame.draw.line(disp.pygame, (128, 255, 128),
                (particles[link.end1_index].pos.x, particles[link.end1_index].pos.y),
                (particles[link.end2_index].pos.x, particles[link.end2_index].pos.y), 2)

    # rendering
    screen_text_FPS = int(timing_clock.get_fps())
    screen_text_FPS2 = disp.font.render("FPS: " + str(screen_text_FPS), True, (255, 255, 255))
    disp.pygame.blit(screen_text_FPS2, (10, 10))
    pygame.display.flip() # swap buffers
    disp.pygame.fill((0, 0, 0))
    timing_clock.tick(90 if disp.cap else 1000000) # 90 FPS

    # exit test
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit() # pygame.quit()
