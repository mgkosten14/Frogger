'''Game class'''
# pylint: disable=wildcard-import, unused-wildcard-import
import arcade
from constants import *

class Game:
    '''Game class'''
    def __init__(self):
        self.paused = False
        self.game_time = DURATION
        self.timer_text = arcade.Text(f"Time: {int(self.game_time)}",
                                      0, 0, TEXT_COLOR, SCALED_SQUARE/2)
        self.timer_text.x = WINDOW_WIDTH-self.timer_text.content_width
        self.points = 0
        self.score_text = arcade.Text(f"Score: {self.points}", 0, 0, TEXT_COLOR, SCALED_SQUARE/2)
        self.level = 1
        self.level_text = arcade.Text(f"Level: {self.level}", self.timer_text.x, SCALED_SQUARE/2,
                                      TEXT_COLOR, SCALED_SQUARE/2)

    def draw_text(self):
        '''Call in on_draw to draw text for GameView'''
        self.timer_text.draw()
        self.level_text.draw()
        self.score_text.draw()
        if self.paused:
            arcade.draw_text("PAUSED", WINDOW_WIDTH/2, WINDOW_HEIGHT/2-SCALED_SQUARE,
                             TEXT_COLOR, SCALED_SQUARE, anchor_x="center")

    def update(self, delta_time):
        '''Call in on_update to update the timer, points, and levels'''
        self.game_time -= delta_time
        self.timer_text.text = f"Time: {int(self.game_time)}"
        self.score_text.text = f"Score: {int(self.points)}"
        self.level_text.text = f"Level: {int(self.level)}"

    def reset(self):
        '''Reset the game to beginning state'''
        self.paused = False
        self.game_time = DURATION
        self.points = 0
        self.level = 1
