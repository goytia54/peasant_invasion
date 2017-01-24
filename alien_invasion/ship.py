import pygame

class Ship(object):
    """Attributes and methods for the ships position and speed"""

    def __init__(self, ai_settings, screen):
        """initialize the ship and set its starting position"""
        self.screen = screen

        #load the ship image and get its rect.
        self.image = pygame.image.load('images/gabe.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.rect.bottom = self.screen_rect.bottom

        # define the inital center as the center of screen
        self.center = self.screen_rect.center

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


    def update(self):
        """ Update the ship's position based on the movement flag. """
        #Depending on the key either move x or y direction
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center = float(self.rect.centerx)
            self.center += self.ai_settings.ship_speed_factor
            self.rect.centerx = self.center
        elif self.moving_left and self.rect.left > 0:
            self.center = float(self.rect.centerx)
            self.center -= self.ai_settings.ship_speed_factor
            self.rect.centerx = self.center
        elif self.moving_up and self.rect.top > 0:
            self.center = float(self.rect.centery)
            self.center -= self.ai_settings.ship_speed_factor
            self.rect.centery = self.center
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center = float(self.rect.centery)
            self.center += self.ai_settings.ship_speed_factor
            self.rect.centery = self.center


    def center_ship(self):
        """center the ship on the screen."""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.rect.bottom = self.screen_rect.bottom


    def blitme(self):
        """draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
        