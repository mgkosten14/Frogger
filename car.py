'''Car class'''
# pylint: disable=wildcard-import, unused-wildcard-import
import arcade
from constants import *

class Car:
    '''
    Class for cars in the road
        car_type: which sprite to show (integer 1-5)
        xpos: center x position of car
    '''
    def __init__(self, car_type, xpos):
        self.speed = 0
        self.car_type = car_type
        self.xpos = xpos
        self.ypos = 0
        self.sprite = None

    def setup(self, spritesheet):
        '''Set texture, speed, and y position based on car_type'''
        match self.car_type:
            case 1:
                vehicle_texture = spritesheet.get_texture(
                    arcade.LBWH(19, 116, SPRITE_SQUARE, SPRITE_SQUARE))
                self.speed = -OBSTACLE_SPEED
                self.ypos = SCALED_SQUARE*2.5
            case 2:
                vehicle_texture = spritesheet.get_texture(
                    arcade.LBWH(55, 116, SPRITE_SQUARE, SPRITE_SQUARE))
                self.speed = OBSTACLE_SPEED
                self.ypos = SCALED_SQUARE*3.5
            case 3:
                vehicle_texture = spritesheet.get_texture(
                    arcade.LBWH(1, 116, SPRITE_SQUARE, SPRITE_SQUARE))
                self.speed = -OBSTACLE_SPEED*1.5
                self.ypos = SCALED_SQUARE*4.5
            case 4:
                vehicle_texture = spritesheet.get_texture(
                    arcade.LBWH(37, 116, SPRITE_SQUARE, SPRITE_SQUARE))
                self.speed = OBSTACLE_SPEED
                self.ypos = SCALED_SQUARE*5.5
            case 5:
                vehicle_texture = spritesheet.get_texture(
                    arcade.LBWH(73, 116, SPRITE_SQUARE * 2, SPRITE_SQUARE))
                self.speed = -OBSTACLE_SPEED*1.5
                self.ypos = SCALED_SQUARE*6.5
            case _:
                raise ValueError('invalid car type, must be integer 1-5')

        self.sprite = arcade.Sprite(vehicle_texture, SCALE, self.xpos, self.ypos)

    def update(self, delta_time, level):
        '''Call in on_update to move the car'''
        self.xpos += self.speed * delta_time * (1 + (0.15 * level))
        if self.xpos > WINDOW_WIDTH + SCALED_SQUARE and self.speed > 0:
            self.xpos = -SCALED_SQUARE
        elif self.xpos < -SCALED_SQUARE and self.speed < 0:
            self.xpos = WINDOW_WIDTH + SCALED_SQUARE

        self.sprite.center_x = self.xpos
