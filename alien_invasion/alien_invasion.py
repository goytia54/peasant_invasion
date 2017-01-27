import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from button import Button
import game_functions as gf


def run_game():
    #initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Peasent Invasion")
    
    #Make the play button.
    play_button = Button(ai_settings, screen, 'Press To Destroy Peasants!')
    #create an instance to store game statistics and create scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    #Make a ship
    ship = Ship(ai_settings, screen)
    #Make a group to store bullets in.
    bullets = Group()
    #Make a group to store peasants in.
    peasants = Group()
    #create the fleet of peasants
    gf.create_fleet(ai_settings, screen, ship, peasants)

    #start the main loop for the game
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        peasants, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, peasants,
                                bullets)
            gf.update_peasants(ai_settings, stats, screen, sb, ship, peasants,
                                bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, peasants,
                        bullets, play_button)

run_game()