'''Fly class'''
# pylint: disable=wildcard-import, unused-wildcard-import
from random import choice
import arcade
from constants import *

class Fly:
    '''Fly class for bonus points'''
    def __init__(self):
        self.xpos = -WINDOW_WIDTH
        self.ypos = -WINDOW_HEIGHT
        self.sprite = None
        self.collected = False
        self.appearance_timer = 0
        self.on_screen = False
        self.empty_homes_x = [SCALED_SQUARE + (SCALED_SQUARE*3*i) for i in range(5)]

    def load_textures(self, spritesheet):
        '''Load fly texture and sprite'''
        fly_texture = spritesheet.get_texture(arcade.LBWH(81, 196, SPRITE_SQUARE, SPRITE_SQUARE))
        self.sprite = arcade.Sprite(fly_texture, SCALE, self.xpos, self.ypos)

    def update(self, delta_time):
        '''Call in on_update to keep the sprite position updated'''
        if not self.collected:
            self.appearance_timer += delta_time
            if self.appearance_timer >= 5:
                if self.on_screen:
                    self.set_offscreen()
                else:
                    self.appear_in_home()

        self.sprite.center_x = self.xpos
        self.sprite.center_y = self.ypos

    def appear_in_home(self):
        '''Choose a random unfilled home and appear there'''
        self.on_screen = True
        self.appearance_timer = 0
        # Move to a random unfilled home
        self.xpos = choice(self.empty_homes_x)
        self.ypos = SCALED_SQUARE * 13.5

    def set_offscreen(self):
        '''Moves the fly off screen'''
        self.on_screen = False
        self.appearance_timer = 0
        # Move offscreen
        self.xpos = -WINDOW_WIDTH
        self.ypos = -WINDOW_HEIGHT

    def level_reset(self):
        '''Resets the fly at the end of a level'''
        self.set_offscreen()
        self.collected = False
        self.empty_homes_x = [SCALED_SQUARE + (SCALED_SQUARE*3*i) for i in range(5)]
