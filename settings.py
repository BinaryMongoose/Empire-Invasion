# noinspection PyAttributeOutsideInit
import json


# noinspection PyAttributeOutsideInit
class Settings:
    """A class to store all settings for TieFighter Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.score_bg_color = (25, 25, 25)

        # Ship settings.
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_color = (240, 0, 0)
        self.bullets_allowed = 3
        self.enemy_fire_rate = 1.0 # Bullets per second

        # TieFighter Settings.
        self.fleet_drop_speed = 10

        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        # How quicly the alien point value increases.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout game."""
        self.ship_speed_factor = 2.5
        self.bullet_speed_factor = 5.5

        self.alien_speed_factor = 1.1

        # fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase the speed settings and alien point values"""

        # stop tieFighters from speeding up too much.

        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
