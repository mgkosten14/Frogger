'''Turt class - named turt instead of turtle to avoid conflict with built-in class'''
# pylint: disable=wildcard-import, unused-wildcard-import
import arcade
from constants import *

class Turt():
    '''
    Class representing a group of turtles in the water
        length: number of turtles in the group
        xpos: center x position of leftmost turtle
    '''
    # We don't agree with pylint setting 7 as an arbitrary limit for instance attributes
    # pylint: disable=too-many-instance-attributes
    def __init__(self, length, xpos):
        super().__init__()
        self.speed = -OBSTACLE_SPEED*1.5
        if length not in [2, 3]:
            raise ValueError('invalid turtle length, must be integer 2 or 3')
        self.length = length
        self.xpos = xpos
        self.ypos = SCALED_SQUARE*8.5 if length == 3 else SCALED_SQUARE*11.5
        self.sprite_list = arcade.SpriteList()
        self.flipped = False

        self.flipped_texture = None
        self.normal_texture = None

    def load_textures(self, spritesheet):
        '''Load turtle textures and sprites'''
        x = self.xpos
        y = self.ypos
        self.normal_texture = spritesheet.get_texture(
            arcade.LBWH(19, 152, SPRITE_SQUARE, SPRITE_SQUARE))
        self.flipped_texture = spritesheet.get_texture(
            arcade.LBWH(73, 152, SPRITE_SQUARE, SPRITE_SQUARE))

        for _ in range(self.length):
            self.sprite_list.append(arcade.Sprite(self.normal_texture, SCALE, x, y))
            x += SCALED_SQUARE

    def update(self, delta_time, level):
        '''Call in on_update to move the turtle group'''
        self.xpos += self.speed * delta_time * (1+ (0.15 * level))
        if self.xpos < -SCALED_SQUARE * self.length:
            self.xpos = WINDOW_WIDTH + SCALED_SQUARE/2

        if self.flipped:
            for sprite in self.sprite_list:
                sprite.texture = self.flipped_texture

        else:
            for sprite in self.sprite_list:
                sprite.texture = self.normal_texture

        x = self.xpos
        for sprite in self.sprite_list:
            sprite.center_x = x
            x += SCALED_SQUARE
