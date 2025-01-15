import pygame
import random
import sys
import math

# Constants for tuning
SEPARATION_RADIUS = 50
COHESION_RADIUS = 100
ALIGNMENT_RADIUS = 100
SEPARATION_COEFFICIENT = 1.5
COHESION_COEFFICIENT = 0.05
ALIGNMENT_COEFFICIENT = 0.1
SOFT_EDGE_MARGIN = 50
SOFT_EDGE_FORCE = 0.5

# Predator settings
PREDATOR_RADIUS = 150
PREDATOR_REPULSION = 2.0


SHOW_DEBUG = False

# Define the Bird class
class Bird:
    def __init__(self, position=None):
        self.max_speed = 3
        self.min_speed = 1
        self.radius = SEPARATION_RADIUS
        self.position = pygame.math.Vector2(position if position else (random.randint(0, 800), random.randint(0, 600)))
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * random.uniform(1, 3)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.size = 10
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )

    def update(self):
        self.velocity += self.acceleration
        speed = self.velocity.length()
        if speed > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed
        elif speed < self.min_speed:
            self.velocity = self.velocity.normalize() * self.min_speed
        self.position += self.velocity
        self.acceleration *= 0  # Reset acceleration each frame

    def apply_behavior(self, birds, predators=None):
        self.separation(birds)
        self.alignment(birds)
        self.cohesion(birds)
        if predators:
            self.avoid_predator(predators)
        self.avoid_edges()

    def separation(self, birds):
        force = pygame.math.Vector2(0, 0)
        for bird in birds:
            distance = self.position.distance_to(bird.position)
            if 0 < distance < SEPARATION_RADIUS:
                diff = self.position - bird.position
                force += diff.normalize() / (distance * distance)
        self.acceleration += force * SEPARATION_COEFFICIENT

    def cohesion(self, birds):
        center_of_mass = pygame.math.Vector2(0, 0)
        count = 0
        for bird in birds:
            distance = self.position.distance_to(bird.position)
            if 0 < distance < COHESION_RADIUS:
                center_of_mass += bird.position
                count += 1
        if count > 0:
            center_of_mass /= count
            force = (center_of_mass - self.position).normalize() * COHESION_COEFFICIENT
            self.acceleration += force

    def alignment(self, birds):
        avg_velocity = pygame.math.Vector2(0, 0)
        count = 0
        for bird in birds:
            distance = self.position.distance_to(bird.position)
            if 0 < distance < ALIGNMENT_RADIUS:
                avg_velocity += bird.velocity
                count += 1
        if count > 0:
            avg_velocity /= count
            force = (avg_velocity - self.velocity).normalize() * ALIGNMENT_COEFFICIENT
            self.acceleration += force

    def avoid_predator(self, predators):
        for predator in predators:
            distance = self.position.distance_to(predator.position)
            if distance < PREDATOR_RADIUS:
                force = (self.position - predator.position).normalize() * (PREDATOR_REPULSION / distance)
                self.acceleration += force

    def avoid_edges(self):
        force = pygame.math.Vector2(0, 0)
        if self.position.x < SOFT_EDGE_MARGIN:
            force.x = SOFT_EDGE_FORCE
        elif self.position.x > 800 - SOFT_EDGE_MARGIN:
            force.x = -SOFT_EDGE_FORCE
        if self.position.y < SOFT_EDGE_MARGIN:
            force.y = SOFT_EDGE_FORCE
        elif self.position.y > 600 - SOFT_EDGE_MARGIN:
            force.y = -SOFT_EDGE_FORCE
        self.acceleration += force

    def draw(self, screen):
        angle = math.atan2(self.velocity.y, self.velocity.x)
        tip = self.position + self.velocity.normalize() * self.size
        left = self.position + self.velocity.normalize().rotate(150) * (self.size / 2)
        right = self.position + self.velocity.normalize().rotate(-150) * (self.size / 2)
        pygame.draw.polygon(screen, self.color, [tip, left, right])
        if SHOW_DEBUG:
            pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius, 1)

# Predator class
class Predator:
    def __init__(self):
        self.position = pygame.math.Vector2((random.randint(0,800), random.randint(0,600)))

    def draw(self, screen):
        pygame.draw.circle(screen, (160, 43, 34), self.position, 5)