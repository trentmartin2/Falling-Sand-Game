import pygame
import random
pygame.init()

# Display Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650
MENU_WIDTH = 200
FPS = 1000

# Gameplay Constants
PARTICLE_SIZE = 1

# Colour definitions
RED = (255, 0, 0)
GREEN =(0, 255, 0)
BLUE = (0, 0, 255)
WHITE =(255, 255, 255)
BLACK = (0, 0, 0)

class FallingSand():
    def __init__(self):
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.run = True
        self.drawing = False
        self.last_spawn_time = 0
        self.spawn_delay = 50
        self.brush_size = 10 # Radius(PARTICLE_SIZE) square
        self.brush_fullness = 25 # Chance to actually spawn a particle when drawing

        # Grid defined as (('x coord', 'y coord'): type{})
        self.grid = {}

        # Particle Selectors
        self.selectors = {
            'red thing': {
                'colour': RED,
                'x coord': SCREEN_WIDTH - 125,
                'y coord': SCREEN_HEIGHT // 4 - 25,
                'width': 50,
                'height': 50
            },
            'green thing': {
                'colour': GREEN,
                'x coord': SCREEN_WIDTH - 125,
                'y coord': SCREEN_HEIGHT // 4 * 2 - 25,
                'width': 50,
                'height': 50
            },
            'blue thing': {
                'colour': BLUE,
                'x coord': SCREEN_WIDTH - 125,
                'y coord': SCREEN_HEIGHT // 4 * 3 - 25,
                'width': 50,
                'height': 50
            }
        }

        # Particle Types and Traits
        self.particle_types = {
            'red thing': {
                'colour': RED
            },
            'green thing': {
                'colour': GREEN
            },
            'blue thing': {
                'colour': BLUE
            }
        }
        self.selected_particle = self.particle_types['red thing']

    def refresh_display(self):
        self.win.fill(BLACK)

        # Particle Rendering
        for (x, y), particle_data in self.grid.items():
            pygame.draw.rect(self.win, particle_data['type']['colour'], (x, y, PARTICLE_SIZE, PARTICLE_SIZE))

        # Menu Border
        pygame.draw.line(self.win, WHITE, (SCREEN_WIDTH - MENU_WIDTH, 0), (SCREEN_WIDTH - MENU_WIDTH, SCREEN_HEIGHT))

        # Selector Rendering
        for selector in self.selectors:
            pygame.draw.rect(self.win, self.selectors[selector]['colour'], (self.selectors[selector]['x coord'], self.selectors[selector]['y coord'], self.selectors[selector]['width'], self.selectors[selector]['height']))
            
        pygame.display.update()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Draws particles if left of menu
                if event.pos[0] < SCREEN_WIDTH - MENU_WIDTH:
                    self.drawing = True

                # Checks if mouse is right of menu
                elif event.pos[0] > SCREEN_WIDTH - MENU_WIDTH:

                    # Iterates through selector dictionary and checks for collision, then sets new particle on click TODO: clean
                    for selector in self.selectors:
                        if event.pos[0] >= self.selectors[selector]['x coord'] and event.pos[0] < self.selectors[selector]['x coord'] + self.selectors[selector]['width'] and event.pos[1] >= self.selectors[selector]['y coord'] and event.pos[1] < self.selectors[selector]['y coord'] + self.selectors[selector]['height']:
                            self.selected_particle = self.particle_types[selector]

            # Disables mousedown tag
            elif event.type == pygame.MOUSEBUTTONUP:
                self.drawing = False
            
            # Allows dragging to draw particles
            #elif event.type == pygame.MOUSEMOTION and self.drawing:
             #   if event.pos[0] < SCREEN_WIDTH - MENU_WIDTH:
              #      self.add_particle(event.pos[0], event.pos[1], self.selected_particle)

            # Loop termination
            elif event.type == pygame.QUIT:
                self.run = False

    def paintbrush(self):
        if self.drawing:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_spawn_time >= self.spawn_delay:
                x, y = pygame.mouse.get_pos()
                if x < SCREEN_WIDTH - MENU_WIDTH:
                    for i in range(-self.brush_size, self.brush_size):
                        for j in range(-self.brush_size, self.brush_size):
                            if x + i < SCREEN_WIDTH - MENU_WIDTH:
                                if random.randint(0, 100) <= self.brush_fullness:
                                    self.add_particle(x + i, y + j, self.selected_particle)
                                    self.last_spawn_time = current_time


    # Handles particle gravity and interation
    def particle_physics(self):
        # Sort from bottom-up so lower particles move first
        for (x, y) in sorted(self.grid.keys(), key=lambda pos: -pos[1]):
            below = (x, y + PARTICLE_SIZE)
            beside_below_left = (x - PARTICLE_SIZE, y + PARTICLE_SIZE)
            beside_below_right = (x + PARTICLE_SIZE, y + PARTICLE_SIZE)
            # Randomization on diagonal fall or horizontal shift to make particle settling look more organic
            rng = random.randint(0, 100)
            spreading_bias = 80
            settling_bias = 80

            # Logic for falling directly down and spreading
            if below not in self.grid and below[1] < SCREEN_HEIGHT:
                if rng >= spreading_bias:
                    leftorright = random.randint(0, 1)
                    if beside_below_left not in self.grid and below[1] < SCREEN_HEIGHT and leftorright == 0:
                        self.grid[beside_below_left] = self.grid[(x, y)]
                        del self.grid[(x, y)]
                    elif beside_below_right not in self.grid and below[1] < SCREEN_HEIGHT and leftorright == 1:
                        self.grid[beside_below_right] = self.grid[(x, y)]
                        del self.grid[(x, y)]
                else:
                    self.grid[below] = self.grid[(x, y)]
                    del self.grid[(x, y)]

            # Left settling logic
            elif (below[0] - PARTICLE_SIZE, below[1]) not in self.grid and below[0] >= 0 and below[1] < SCREEN_HEIGHT:
                if rng <= settling_bias:
                    self.grid[(below[0] - PARTICLE_SIZE, below[1])] = self.grid[(x, y)]
                    del self.grid[(x, y)]

                # Chance to shift directly left
                elif (below[0] - PARTICLE_SIZE, below[1] - PARTICLE_SIZE) not in self.grid and below[0] >= 0 and below[1] - PARTICLE_SIZE < SCREEN_HEIGHT:
                    self.grid[(below[0] - PARTICLE_SIZE, below[1] - PARTICLE_SIZE)] = self.grid[(x, y)]
                    del self.grid[(x, y)]

            # Right settling logic
            elif (below[0] + PARTICLE_SIZE, below[1]) not in self.grid and below[0] < SCREEN_WIDTH - MENU_WIDTH - PARTICLE_SIZE and below[1] < SCREEN_HEIGHT:
                if rng <= settling_bias:
                    self.grid[(below[0] + PARTICLE_SIZE, below[1])] = self.grid[(x, y)]
                    del self.grid[(x, y)]

                # Chance to shift directly right
                elif (below[0] + PARTICLE_SIZE, below[1] - PARTICLE_SIZE) not in self.grid and below[0] >= 0 and below[1] - PARTICLE_SIZE < SCREEN_HEIGHT:
                    self.grid[(below[0] + PARTICLE_SIZE, below[1] - PARTICLE_SIZE)] = self.grid[(x, y)]
                    del self.grid[(x, y)]

    # Adds particle to list and snaps to grid
    def add_particle(self, x, y, type):
        x -= x % PARTICLE_SIZE
        y -= y % PARTICLE_SIZE
        key = (x, y)
        if key not in self.grid:
            self.grid[key] = {'type': type}

game = FallingSand()

while game.run:
    game.clock.tick(FPS)
    game.event_handler()
    game.paintbrush()
    game.particle_physics()
    game.refresh_display()

pygame.quit()
