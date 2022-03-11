import sys
from time import sleep
import os
import json
from random import randint

import pygame
from bullet import Bullet
from tiefighter import TieFighter

pygame.mixer.init()

s = 'sounds'
shot = pygame.mixer.Sound(os.path.join(s, 'gunshot.ogg'))


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to key presses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # pygame.mixer.Sound.play(shot)
        fire_ship_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, tieFighters, bullets):
    """Respond to key presses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("high_score.json", "w") as f_obj:
                json.dump(stats.high_score, f_obj)

            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, tieFighters, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, tieFighters, bullets, mouse_x, mouse_y):
    """Start a new game when player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of tieFighters and bullets.
        tieFighters.empty()
        bullets.empty()

        # Create a new fleet and center ship.
        create_fleet(ai_settings, screen, ship, tieFighters)


def update_screen(ai_settings, screen, stats, sb, ship, tieFighters, bullets, tieFighterBullets, play_button):
    # Redraw the screen during each pass
    screen.fill(ai_settings.bg_color)
    draw_background(screen)

    # Redraw all bullets behind ships and tieFighters
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for tieFighterBullet in tieFighterBullets.sprites():
        tieFighterBullet.draw_bullet()

    ship.blitme()
    tieFighters.draw(screen)

    # Draw the score information
    pygame.draw.rect(screen, ai_settings.score_bg_color, pygame.Rect(0, 0, 1200, 130))
    sb.show_score()

    # Display the play button if game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def draw_background(screen):
    image = pygame.image.load("images/Background.bmp")
    rect = image.get_rect()
    image_size = 200

    for i in range(0, 4):
        for j in range(0, 6):
            screen.blit(image, rect)
            rect.x += image_size
        rect.x = 0
        rect.y += image_size


def fire_tieFighter_bullet(ai_settings, screen, tieFighter, tieFighters, tieFighterBullets):
    if randint(0, len(tieFighters)) == randint(0, len(tieFighters)):
        if len(tieFighterBullets) < ai_settings.bullets_allowed:
            fire_bullet(ai_settings, screen, tieFighter, tieFighterBullets)


def fire_ship_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        fire_bullet(ai_settings, screen, ship, bullets)


def fire_bullet(ai_settings, screen, sprite, bullets):
    # Create a new bullet and add it to the bullets group
    new_bullet = Bullet(ai_settings, screen, sprite)
    bullets.add(new_bullet)


def update_bullets(ai_settings, screen, stats, sb, ship, tieFighters, bullets, tieFighterBullets):
    """Update position of bullets and get rid of old bullets."""
    bullets.update(False)
    tieFighterBullets.update(True)

    # Get rid of old bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    for bullet in tieFighterBullets.copy():
        if bullet.rect.bottom >= ai_settings.screen_height:
            tieFighterBullets.remove(bullet)

    # Check if any bullets have hit tieFighters.
    # If so, get rid of the bullet and tieFighters
    ship_tieFighter_collisions = pygame.sprite.groupcollide(bullets, tieFighters, True, True)

    ship_is_hit = pygame.sprite.spritecollide(ship, tieFighterBullets, False)

    if ship_tieFighter_collisions:
        for tieFighters in ship_tieFighter_collisions.values():
            # noinspection PyTypeChecker
            stats.score += ai_settings.alien_points * len(tieFighters)
            sb.prep_score()
        check_high_score(stats, sb)

    if ship_is_hit:
        ship_hit(ai_settings, screen, stats, sb, ship, tieFighters, bullets, tieFighterBullets)

    if len(tieFighters) == 0:
        new_level(ai_settings, screen, stats, sb, ship, tieFighters, bullets, tieFighterBullets)


def new_level(ai_settings, screen, stats, sb, ship, tieFighters, bullets, tieFighterBullets):
    # If entre fleet is destroyed, start a new level
    bullets.empty()
    tieFighterBullets.empty()
    ai_settings.increase_speed()

    # Increase level
    stats.level += 1
    sb.prep_level()
    create_fleet(ai_settings, screen, ship, tieFighters)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of tieFighters that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_tieFighters_x(ai_settings, alien_width):
    """Determine the number of tieFighters that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_tieFighter(ai_settings, screen, aliens, tieFighter_number, row_number):
    """Create an alien and place it in a row."""
    # Create an alien and place it in a row
    tieFighter = TieFighter(ai_settings, screen)
    tieFighter_width = tieFighter.rect.width
    tieFighter.x = tieFighter_width + 2 * tieFighter_width * tieFighter_number
    tieFighter.rect.x = tieFighter.x
    tieFighter.rect.y = tieFighter.rect.height + 2 * tieFighter.rect.height * row_number
    aliens.add(tieFighter)


def create_fleet(ai_settings, screen, ship, tieFighters):
    """Create a full fleet of tieFighters."""
    # Create an alien and find the number of tieFighters in a row
    alien = TieFighter(ai_settings, screen)
    number_aliens_x = get_number_tieFighters_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the first row of tieFighters
    for row_number in range(number_rows):
        for tieFighter_number in range(number_aliens_x):
            create_tieFighter(ai_settings, screen, tieFighters, tieFighter_number, row_number)


def check_fleet_edges(ai_settings, tieFighters, screen, tieFighterBullets):
    """Respond appropriately if any tieFighters have reached the edge."""
    for tieFighter in tieFighters.sprites():
        if tieFighter.check_edges():
            change_fleet_direction(ai_settings, tieFighters)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, tieFighterBullets):
    """Respond to ship being hit by Tie-Fighter"""
    if stats.ships_left > 0:
        # Decrement ships left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Empty the list of tieFighters and bullets.
        aliens.empty()
        bullets.empty()
        tieFighterBullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_tie_fighters_bottom(ai_settings, screen, stats, sb, ship, tieFighters, bullets, tieFighterBullets):
    """Check if any tieFighters have gotten to the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in tieFighters:
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this as if the ship was hit
            ship_hit(ai_settings, screen, stats, sb, ship, tieFighters, bullets, tieFighterBullets)
            break


def update_tieFighters(ai_settings, screen, stats, sb, ship, tieFighters, bullets, tieFighterBullets):
    """
    Check if the fleet is at an edge,
       and then update the positions of all tieFighters in the fleet.
    """
    check_fleet_edges(ai_settings, tieFighters, screen, tieFighterBullets)
    tieFighters.update()

    for tieFighter in tieFighters:
        fire_tieFighter_bullet(ai_settings, screen, tieFighter, tieFighters, tieFighterBullets)

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, tieFighters):
        ship_hit(ai_settings, screen, stats, sb, ship, tieFighters, bullets, tieFighterBullets)

    check_tie_fighters_bottom(ai_settings, screen, stats, sb, ship, tieFighters, bullets, tieFighterBullets)


def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
