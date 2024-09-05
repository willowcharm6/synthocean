import pygame
import time
import random
import math

class Consumer(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 300
        self.hunger = 100
        self.age = 0
        self.reproductive_urge = 0
        self.last_reproduce_time = time.time()
        self.last_hunger_time = time.time()
        self.last_move_time = time.time()
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, producers):
        current_time = time.time()

        # Update hunger
        if current_time - self.last_hunger_time > 1:
            self.hunger -= 1
            self.last_hunger_time = current_time

        # Update age
        self.age += 1 / 60  # Assuming 60 FPS

        # Reproductive urge
        if current_time - self.last_reproduce_time > 5:
            self.reproductive_urge += 1
            self.last_reproduce_time = current_time
            if self.reproductive_urge > 20:
                self.reproductive_urge = 0  # Reset urge
                self.look_for_mate()

        # Check for death
        if self.age > 300:  # 5 minutes = 300 seconds
            self.kill()    

        # Random movement
        if current_time - self.last_move_time > 0.0001:
            self.rect.x += random.choice([-5, 5])
            self.rect.y += random.choice([-5, 5])
            self.last_move_time = current_time
        
        self.apply_periodic_boundary()

        # Check distance to producers and move towards them if within 8 pixels
        for producer in producers:
            if self.rect.colliderect(producer.rect.inflate(100, 100)):
                self.move_towards(producer)
                if self.rect.colliderect(producer.rect):
                    producer.kill()
    
    def apply_periodic_boundary(self):
        # Wrap the Consumer around if it moves out of screen boundaries
        if self.rect.right < 0:
            self.rect.left = self.screen_width
        elif self.rect.left > self.screen_width:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = self.screen_height
        elif self.rect.top > self.screen_height:
            self.rect.bottom = 0
        

    def move_towards(self, producer):
        # Move towards the producer
        dx = producer.rect.centerx - self.rect.centerx
        dy = producer.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > 0:
            dx /= distance
            dy /= distance

            self.rect.x += dx * 2
            self.rect.y += dy * 2

    def look_for_mate(self):
        print("Looking for a mate...")
