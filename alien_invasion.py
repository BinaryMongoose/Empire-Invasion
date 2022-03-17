import pygame
import json
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
import game_functions as gf


def runGame():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("TieFighter Invasion")

    # Make the play button.
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game stats and create a scoreboard
    stats = GameStats(ai_settings)
    with open("high_score.json") as f_obj:
        stats.high_score = json.load(f_obj)

    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship, a group of bullets, and a group of tieFighters.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    tieFighterBullets = Group()
    tieFighters = Group()

    gf.create_fleet(ai_settings, screen, ship, tieFighters)

    # Start the main loop for the game.
    start_time = pygame.time.get_ticks()
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, tieFighters, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, tieFighters, bullets, tieFighterBullets)
            gf.update_tieFighters(ai_settings, screen, stats, sb, ship, tieFighters, bullets, tieFighterBullets)

        end_time = pygame.time.get_ticks()
        delta_time = end_time - start_time
        start_time = end_time
        gf.update_screen(ai_settings, screen, stats, sb, ship, tieFighters, bullets, tieFighterBullets, play_button, delta_time)


runGame()
