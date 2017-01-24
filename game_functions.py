import sys
from time import sleep

import pygame

from bullet import Bullet
from peasant import Peasant

def get_number_rows(ai_settings, ship_height, peasant_height):
    """Determine the number of rows of peasants that fit on screen """
    available_space_y = (ai_settings.screen_height -
                        (3 * peasant_height))
    number_rows = int(available_space_y / (2* peasant_height))
    return number_rows


def get_number_peasants_x(ai_settings, peasant_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - peasant_width
    number_peasant_x = int(available_space_x / (peasant_width * 2))
    return number_peasant_x


def create_peasant(ai_settings, screen, peasants, peasant_number, row_number):
    """ Create a peasant and place it in the row """
    peasant = Peasant(ai_settings, screen)
    peasant_width = peasant.rect.width
    peasant.x = peasant_width + 2 * peasant_width * peasant_number
    peasant.rect.x = peasant.x
    peasant.rect.y = peasant.rect.height + 2 * peasant.rect.height * row_number
    peasants.add(peasant)


def create_fleet(ai_settings, screen, ship, peasants):
    """create a full fleet of aliens"""
    # Create an peasant and find the number of peasants in a row
    peasant = Peasant(ai_settings, screen)
    number_peasant_x = get_number_peasants_x(ai_settings, peasant.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, peasant.rect.height)
    # Create the first row of aliens
    for row_number in xrange(number_rows):
        for peasant_number in xrange(number_peasant_x):
            create_peasant(ai_settings, screen, peasants, peasant_number, 
                            row_number)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Responds to keypresses"""
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move the ship to the right
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """ Responds to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, stats, play_button, ship, peasants, 
                bullets):
    """checks for keyboard and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, 
                                peasants, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, play_button, ship, peasants,
                        bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #reset the game settings.
        ai_settings.initialize_dynamic_settings()

        #Hide the mouse cursor
        pygame.mouse.set_visible(False)
        # reset the game statisitics
        stats.reset_stats()
        stats.game_active = True

        peasants.empty()
        bullets.empty()

        #create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, peasants)
        ship.center_ship()


def check_fleet_edges(ai_settings, peasants):
    """Respond differently if any peasants have reached the edge"""
    for peasant in peasants.sprites():
        if peasant.check_edges():
            change_fleet_direction(ai_settings, peasants)
            break

def change_fleet_direction(ai_settings, peasants):
    """ Drop the entire fleet and change the fleet's direction."""
    for peasant in peasants.sprites():
        peasant.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if the limit is not reached yet"""
    #Create a new bullet and add it to the bullet group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, sb, ship, peasant, bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    #Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    #Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #draws the ship at current location
    ship.blitme()
    peasant.draw(screen)

    #Draw the score information
    sb.show_score()

    #Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    #Make the most recently drawn screen visible
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, peasants, bullets):
    """Update the position of bullets and get rid of old bullets"""
    #Update bullet positions.
    bullets.update()
    #Get rid of bullets that have dissappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_peasant_collision(ai_settings, screen, ship, peasants, bullets)

def check_bullet_peasant_collision(ai_settings, screen, ship, peasants, bullets):
    """respond to bullet-peasant collisions."""
    #if so, get rid of the bullet and peasants
    collisions = pygame.sprite.groupcollide(bullets, peasants, True, True)
    if len(peasants) == 0:
        #Destroy existing  bullets, speed up game and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, peasants)


def ship_hit(ai_settings, stats, screen, ship, peasants, bullets):
    """Respond to ship being hit by peasant."""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        #empty the list of peasants and bullets.
        peasants.empty()
        bullets.empty()
        #create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, peasants)
        ship.center_ship()
        #pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_peasants_bottom(ai_settings, stats, screen, ship, peasants, bullets):
    """ check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for peasant in peasants.sprites():
        if peasant.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, ship, peasants, bullets)


def update_peasants(ai_settings, stats, screen, ship, peasants, bullets):
    """update the positions of all peasants"""
    check_fleet_edges(ai_settings, peasants)
    peasants.update()
    # look for peasants hitting the bottom of the screen.
    check_peasants_bottom(ai_settings, stats, screen, ship, peasants, bullets)

    #Look for peasant-ship collisions
    if pygame.sprite.spritecollideany(ship, peasants):
        ship_hit(ai_settings, stats, screen, ship, peasants, bullets)
