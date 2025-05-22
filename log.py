'''Log class'''
# pylint: disable=wildcard-import, unused-wildcard-import
import arcade
from constants import *

class Log:
    '''
    Class for logs in the water
        log_type: LogType enum (SHORT, MEDIUM, or LONG)
        xpos: center x position of leftmost log sprite
    '''
    def __init__(self, log_type, xpos):
        self.speed = 0
        self.length = 0
        self.xpos = xpos
        self.ypos = 0
        self.sprite_list = arcade.SpriteList()

        match log_type:
            case LogType.SHORT:
                self.speed = OBSTACLE_SPEED
                self.length = 3
                self.ypos = SCALED_SQUARE*9.5
            case LogType.MEDIUM:
                self.speed = OBSTACLE_SPEED*1.5
                self.length = 4
                self.ypos = SCALED_SQUARE*12.5
            case LogType.LONG:
                self.speed = OBSTACLE_SPEED*2
                self.length = 6
                self.ypos = SCALED_SQUARE*10.5
            case _:
                raise ValueError('invalid log type, must be LogType enum (SHORT, MEDIUM, or LONG)')


    def load_textures(self, spritesheet):
        '''Load log textures and sprites'''
        x = self.xpos
        y = self.ypos
        left_log = spritesheet.get_texture(arcade.LBWH(1, 134, SPRITE_SQUARE, SPRITE_SQUARE))
        mid_log = spritesheet.get_texture(arcade.LBWH(19, 134, SPRITE_SQUARE, SPRITE_SQUARE))
        right_log = spritesheet.get_texture(arcade.LBWH(37, 134, SPRITE_SQUARE, SPRITE_SQUARE))

        self.sprite_list.append(arcade.Sprite(left_log, SCALE, x, y))
        x += SCALED_SQUARE
        for _ in range(self.length - 2):
            self.sprite_list.append(arcade.Sprite(mid_log, SCALE, x, y))
            x += SCALED_SQUARE
        self.sprite_list.append(arcade.Sprite(right_log, SCALE, x, y))

    def update(self, delta_time, level):
        '''Call in on_update to move the log'''
        self.xpos += self.speed * delta_time * (1 + (0.15 * level))
        if self.xpos > WINDOW_WIDTH + SCALED_SQUARE:
            self.xpos = -SCALED_SQUARE * self.length

        x = self.xpos
        for sprite in self.sprite_list:
            sprite.center_x = x
            x += SCALED_SQUARE
