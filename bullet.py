import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_settings, screen, sprite):
        """Create a bullet object at the ships current position"""
        super(Bullet, self).__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct position.
        self.image = pygame.image.load("images/ship_bullet.bmp")
        self.rect = self.image.get_rect()
        self.rect.centerx = sprite.rect.centerx
        self.rect.top = sprite.rect.top

        # Store a bullets position as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self, isTieFighter):
        """Move the bullet up the screen"""
        # Update the decimal position of the bullet
        if isTieFighter:
            self.image = pygame.image.load("images/Tie-Fighter-Bullet.bmp")
            self.y += self.speed_factor
        else:
            self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        self.screen.blit(self.image, self.rect)
