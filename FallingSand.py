import pygame
import random
pygame.init()

# Display Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650
MENU_WIDTH = 200
FPS = 1000

# Gameplay Constants
PARTICLE_SIZE = 10

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

        # Particle defined as (x coord, y coord, type)
        self.particles = []

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
        for particle in self.particles:
            pygame.draw.rect(self.win, particle[2]['colour'], (particle[0], particle[1], PARTICLE_SIZE, PARTICLE_SIZE))

        # Menu Border
        pygame.draw.line(self.win, WHITE, (SCREEN_WIDTH - MENU_WIDTH, 0), (SCREEN_WIDTH - MENU_WIDTH, SCREEN_HEIGHT))

        # Selector Rendering
        for i in self.selectors:
            pygame.draw.rect(self.win, self.selectors[i]['colour'], (self.selectors[i]['x coord'], self.selectors[i]['y coord'], self.selectors[i]['width'], self.selectors[i]['height']))
            
        pygame.display.update()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Draws particles if left of menu
                if event.pos[0] < SCREEN_WIDTH - MENU_WIDTH:
                    self.drawing = True
                    self.add_particle(event.pos[0], event.pos[1], self.selected_particle)

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
            elif event.type == pygame.MOUSEMOTION and self.drawing:
                if event.pos[0] < SCREEN_WIDTH - MENU_WIDTH:
                    self.add_particle(event.pos[0], event.pos[1], self.selected_particle)

            # Loop termination
            elif event.type == pygame.QUIT:
                self.run = False

    # Adds particle to list and snaps to grid
    def add_particle(self, x, y, type):
        x_diff = x % PARTICLE_SIZE
        y_diff = y % PARTICLE_SIZE
        x = x - x_diff
        y = y - y_diff
        self.particles.append((x, y, type))

game = FallingSand()

while game.run:
    game.clock.tick(FPS)
    game.event_handler()
    game.refresh_display()

pygame.quit()
