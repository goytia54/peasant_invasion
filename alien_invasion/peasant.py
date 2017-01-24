import pygame 
from pygame.sprite import Sprite

class Peasant(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_settings, screen):
        """Intialize the alien and set its starting positions."""
        super(Peasant, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #load the alien image and set its rect attribute
        self.image = pygame.image.load('images/xbox.bmp')
        self.rect = self.image.get_rect()

        #set peasant at the 0,0 pixel
        self.rect.x = 0 
        self.rect.y = 0

        #store the aliens exact position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Retun True if alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """move alien left or right"""
        self.x += (self.ai_settings.peasant_speed_factor *
                        self.ai_settings.fleet_direction)
        self.rect.x = self.x


    def blitme(self):
        """Draw the peasant at its current position"""
        self.screen.blit(self.image, self.rect)

