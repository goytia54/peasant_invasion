class Settings(object):
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """initializes the game's settings"""
        #screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)
        #ship Settings
        self.ship_speed_factor = 8.0
        #bullet Settings
        self.bullet_speed_factor = 10.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (230, 0, 0)
        self.bullets_allowed = 4

