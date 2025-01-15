import pygame
import sys
from boids_algo import Bird, Predator
import pygame_widgets as pw

SHOW_DEBUG = False

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Enhanced Boids Simulation")
clock = pygame.time.Clock()

# Create a flock of birds and a predator
birds = []
predators = []

button_x = 150
button_y = 150
button_width = 100
button_height = 40
button_color = (100, 100, 100)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            SHOW_DEBUG = not SHOW_DEBUG
        if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + button_height:
            if event.type == pygame.MOUSEBUTTONDOWN:
                predator = Predator()
                predators.append(predator)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird = Bird(mouse)
                birds.append(bird)


    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))

    for predator in predators:
        predator.draw(screen)

    for bird in birds:
        bird.apply_behavior(birds, predators)
        bird.update()
        bird.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()