import pygame
import random
import sys

# Define the Bird class
class Bird:
    def __init__(self, position=None):
        self.position = position
        self.velocity = pygame.math.Vector2(
            random.uniform(-5, 5), 
            random.uniform(-5, 5)
        ).normalize() * random.uniform(1, 3)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.size = 5
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        self.acceleration *= 0  # Reset acceleration each frame

    def wrap_around(self, screen_width, screen_height):
        # Make the bird appear on the opposite side if it moves off-screen
        if self.position.x > screen_width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = screen_width
        if self.position.y > screen_height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = screen_height

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.size)


# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Boids Simulation")
clock = pygame.time.Clock()

# Create a flock of birds
birds = []

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            bird = Bird(pygame.mouse.get_pos())
            birds.append(bird)

    # Update birds
    for bird in birds:
        bird.update()
        bird.wrap_around(screen_width, screen_height)

    # Draw everything
    screen.fill((0, 0, 0))  # Clear screen with black background
    for bird in birds:
        bird.draw(screen)
    pygame.display.flip()

    for i, bird1 in enumerate(birds):
        for j, bird2 in enumerate(birds):
            if i != j and bird1.position.distance_to(bird2.position) < 20:
                bird1.velocity = bird1.velocity*-1
                bird2.velocity = bird2.velocity*-1
    for i, bird1 in enumerate(birds):
        for j, bird2 in enumerate(birds):
            if i != j and bird1.position.distance_to(bird2.position) < 200:
                bird1.velocity = bird2.velocity


    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()