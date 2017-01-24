class Settings(object):
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """initializes the game's settings"""
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (70, 130, 180)
        #ship Settings
        self.ship_speed_factor = 2.0
        self.ship_limit = 3
        #bullet Settings
        self.bullet_speed_factor = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (230, 0, 0)
        self.bullets_allowed = 4
        # Alien Settings
        self.peasant_speed_factor = 1
        self.fleet_drop_speed = 10
        #fleet direction of 1 represents right, -1 left
        self.fleet_direction = 1

        #how quickly the game speeds up
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.peasant_speed_factor = 1

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.peasant_speed_factor *= self.speedup_scale
        