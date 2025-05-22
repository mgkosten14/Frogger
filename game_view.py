'''Frogger game implemented using Python Arcade.'''
# pylint: disable=wildcard-import, unused-wildcard-import
import os
import arcade
from firebase import firebase_access, add_entry, get_top_five
from constants import *
from game import Game
from frog import Frog
from turt import Turt
from log import Log
from car import Car
from fly import Fly

class InstructionView(arcade.View):
    """Creates the introduction screen of the game."""
    def __init__(self):
        super().__init__()

        # Making CRT Filter
        self.crt_filter = arcade.experimental.crt_filter.CRTFilter(FILTER_WIDTH, FILTER_HEIGHT,
                                                                   DSCALE, SCAN, PIX, WARP,
                                                                   DARKMASK, LIGHTMASK)

    def on_show_view(self):
        self.window.background_color = arcade.csscolor.BLACK

    def on_draw(self):
        if FILTER_ON:
            self.crt_filter.use()
            self.crt_filter.clear()

            arcade.draw_text("Controls", WINDOW_WIDTH/2, WINDOW_HEIGHT-SCALED_SQUARE*2,
                             TEXT_COLOR, SCALED_SQUARE*2, anchor_x='center')
            arcade.draw_text("W/Up = Move up\nA/Left = Move left\nS/Down = Move down\n"
                             "D/Right = Move right\nSpace = Pause/Unpause", WINDOW_WIDTH/2,
                             WINDOW_HEIGHT-SCALED_SQUARE*4, TEXT_COLOR, SCALED_SQUARE,
                             anchor_x='center', multiline=True, width=WINDOW_WIDTH, align="center")
            arcade.draw_text("Press the Space Bar to play!", WINDOW_WIDTH/2,
                             SCALED_SQUARE*3, TEXT_COLOR, SCALED_SQUARE, anchor_x='center',
                             multiline=True, width=WINDOW_WIDTH, align="center")
            # CRT filter applied.
            self.window.use()
            self.clear()
            self.crt_filter.draw()
        else:
            self.clear()
            arcade.draw_text("Controls", WINDOW_WIDTH/2, WINDOW_HEIGHT-SCALED_SQUARE*2,
                             TEXT_COLOR, SCALED_SQUARE*2, anchor_x='center')
            arcade.draw_text("W/Up = Move up\nA/Left = Move left\nS/Down = Move down\n"
                             "D/Right = Move right\nSpace = Pause/Unpause", WINDOW_WIDTH/2,
                             WINDOW_HEIGHT-SCALED_SQUARE*4, TEXT_COLOR, SCALED_SQUARE,
                             anchor_x='center', multiline=True, width=WINDOW_WIDTH, align="center")
            arcade.draw_text("Press the Space Bar to play!", WINDOW_WIDTH/2,
                             SCALED_SQUARE*3, TEXT_COLOR, SCALED_SQUARE, anchor_x='center',
                             multiline=True, width=WINDOW_WIDTH, align="center")

    def on_key_press(self, symbol, _):
        if symbol == arcade.key.SPACE:
            game_view = GameView()
            game_view.make_objects()
            game_view.load_textures()
            self.window.show_view(game_view)
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

class GameView(arcade.View):
    '''GameView class for running and displaying the game'''
    # We don't agree with pylint setting 7 as an arbitrary limit for instance attributes
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        super().__init__()

        # Define Textures dictionary
        self.textures = {}

        # home frog count
        self.frog_home_count = 0

        # death animation
        self.current_animation_index = 0
        self.frog_death_x = 0
        self.frog_death_y = 0

        # max y value of frog player through each level
        self.max_frog_y = SCALED_SQUARE*1.5

        self.turtle_flip_timer = FLIP_DELAY

        # Creating Containers for obstacles (and player)
        self.player = Frog()
        self.fly = Fly()
        self.turtles = []
        self.logs = []
        self.cars = []
        self.frog_homes = []
        self.death_animations = []

        # Creating SpriteList
        self.sprite_list = arcade.SpriteList()
        self.car_sprites = arcade.SpriteList()
        self.turtle_sprites = arcade.SpriteList()
        self.log_sprites = arcade.SpriteList()
        self.frog_home_sprites = arcade.SpriteList()
        self.death_frog_sprites = arcade.SpriteList()

        # Creating timer and game backend
        self.backend = Game()

        # Making CRT Filter
        self.crt_filter = arcade.experimental.crt_filter.CRTFilter(FILTER_WIDTH, FILTER_HEIGHT,
                                                                   DSCALE, SCAN, PIX, WARP,
                                                                   DARKMASK, LIGHTMASK)

    def load_background_textures(self, spritesheet):
        '''Loads background textures from the spritesheet into the textures dictionary'''
        self.textures['water'] = spritesheet.get_texture(arcade.LBWH(1, 390, 28, 32))
        self.textures['median'] = spritesheet.get_texture(
            arcade.LBWH(135, 196, SPRITE_SQUARE, SPRITE_SQUARE))
        self.textures['homes'] = spritesheet.get_texture(
            arcade.LBWH(1, 188, SPRITE_SQUARE*2, SPRITE_SQUARE*1.5))
        self.textures['grass'] = spritesheet.get_texture(
            arcade.LBWH(35, 188, SPRITE_SQUARE*.5, SPRITE_SQUARE*1.5))
        # Title Letters
        self.textures['title_f'] = spritesheet.get_texture(
            arcade.LBWH(1, 232, SPRITE_SQUARE, SPRITE_SQUARE))
        self.textures['title_r'] = spritesheet.get_texture(
            arcade.LBWH(19, 232, SPRITE_SQUARE, SPRITE_SQUARE))
        self.textures['title_o'] = spritesheet.get_texture(
            arcade.LBWH(37, 232, SPRITE_SQUARE, SPRITE_SQUARE))
        self.textures['title_g'] = spritesheet.get_texture(
            arcade.LBWH(55, 232, SPRITE_SQUARE, SPRITE_SQUARE))
        self.textures['title_e'] = spritesheet.get_texture(
            arcade.LBWH(73, 232, SPRITE_SQUARE, SPRITE_SQUARE))
        # Lives tracker
        self.textures['lives'] = spritesheet.get_texture(
            arcade.LBWH(37, 214, SPRITE_SQUARE/2, SPRITE_SQUARE/2))

    def load_textures(self):
        '''Loads sprite textures from the spritesheet'''
        # Load the spritesheet - https://www.spriters-resource.com/arcade/frogger/sheet/11067/
        spritesheet = arcade.load_spritesheet('assets/spritesheet_transparent.png')

        self.load_background_textures(spritesheet)

        # Load all textures and add to sprite lists
        for log in self.logs:
            log.load_textures(spritesheet)
            self.log_sprites.extend(log.sprite_list)

        for car in self.cars:
            car.setup(spritesheet)
            self.car_sprites.append(car.sprite)

        for turtle in self.turtles:
            turtle.load_textures(spritesheet)
            self.turtle_sprites.extend(turtle.sprite_list)

        for frog_home in self.frog_homes:
            frog_home.load_textures(spritesheet, 'frog_down')
            self.frog_home_sprites.append(frog_home.sprite)

        self.fly.load_textures(spritesheet)
        self.sprite_list.append(self.fly.sprite)

        # Adding obstacle sprites to main sprite list
        self.sprite_list.extend(self.log_sprites)
        self.sprite_list.extend(self.car_sprites)
        self.sprite_list.extend(self.turtle_sprites)
        self.sprite_list.extend(self.frog_home_sprites)

        for i, death_anim in enumerate(self.death_animations):
            death_anim.load_textures(spritesheet, ('death_animation_' + str(i + 1)))
            self.death_frog_sprites.append(death_anim.sprite)

        self.player.load_textures(spritesheet, 'frog_up')
        self.sprite_list.append(self.player.sprite)

    def draw_background(self):
        '''Draws the background image including median strips and ending homes.'''
        arcade.draw_texture_rect(self.textures['water'],
                                 arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        # Draw the title
        title_x = WINDOW_WIDTH/2-SCALED_SQUARE*3.5
        title_y = SCALED_SQUARE*14.75
        arcade.draw_texture_rect(self.textures['title_f'],
                                 arcade.LBWH(title_x, title_y, SCALED_SQUARE, SCALED_SQUARE))
        title_x += SCALED_SQUARE
        arcade.draw_texture_rect(self.textures['title_r'],
                                 arcade.LBWH(title_x, title_y, SCALED_SQUARE, SCALED_SQUARE))
        title_x += SCALED_SQUARE
        arcade.draw_texture_rect(self.textures['title_o'],
                                 arcade.LBWH(title_x, title_y, SCALED_SQUARE, SCALED_SQUARE))
        title_x += SCALED_SQUARE
        arcade.draw_texture_rect(self.textures['title_g'],
                                 arcade.LBWH(title_x, title_y, SCALED_SQUARE, SCALED_SQUARE))
        title_x += SCALED_SQUARE
        arcade.draw_texture_rect(self.textures['title_g'],
                                 arcade.LBWH(title_x, title_y, SCALED_SQUARE, SCALED_SQUARE))
        title_x += SCALED_SQUARE
        arcade.draw_texture_rect(self.textures['title_e'],
                                 arcade.LBWH(title_x, title_y, SCALED_SQUARE, SCALED_SQUARE))
        title_x += SCALED_SQUARE
        arcade.draw_texture_rect(self.textures['title_r'],
                                 arcade.LBWH(title_x, title_y, SCALED_SQUARE, SCALED_SQUARE))
        # Draw medians and homes
        for x in range(0, WINDOW_WIDTH, SCALED_SQUARE):
            # Draw medians
            arcade.draw_texture_rect(self.textures['median'],
                                     arcade.LBWH(x, SCALED_SQUARE, SCALED_SQUARE, SCALED_SQUARE))
            arcade.draw_texture_rect(self.textures['median'],
                                     arcade.LBWH(x, SCALED_SQUARE*7, SCALED_SQUARE, SCALED_SQUARE))
            # Draw homes
            if x % (SCALED_SQUARE*3) == 0:
                arcade.draw_texture_rect(self.textures['homes'],
                                         arcade.LBWH(x, SCALED_SQUARE*13,
                                                     SCALED_SQUARE*2, SCALED_SQUARE*1.5))
            if x % (SCALED_SQUARE*3) == SCALED_SQUARE*2:
                arcade.draw_texture_rect(self.textures['grass'],
                                         arcade.LBWH(x, SCALED_SQUARE*13,
                                                     SCALED_SQUARE*.5, SCALED_SQUARE*1.5))
                arcade.draw_texture_rect(self.textures['grass'],
                                         arcade.LBWH(x+SCALED_SQUARE*.5, SCALED_SQUARE*13,
                                                     SCALED_SQUARE*.5, SCALED_SQUARE*1.5))
        # Draw remaining lives
        for i in range(self.player.lives):
            arcade.draw_texture_rect(self.textures['lives'],
                                     arcade.LBWH(i*SCALED_SQUARE*.5, SCALED_SQUARE*.5,
                                                 SCALED_SQUARE*.5, SCALED_SQUARE*.5))

    def make_objects(self):
        '''Create obstacles: cars, logs, and turtles'''
        for i in range(4):
            self.turtles.append(Turt(3, SCALED_SQUARE*4*i))
            self.turtles.append(Turt(2, WINDOW_WIDTH-SCALED_SQUARE*3.5*i))

        for i in range(3):
            self.cars.append(Car(1, SCALED_SQUARE*4.5*i))
            self.cars.append(Car(2, WINDOW_WIDTH-SCALED_SQUARE*4*i))
            self.cars.append(Car(3, WINDOW_WIDTH-SCALED_SQUARE*4*i))
            self.cars.append(Car(4, SCALED_SQUARE*4.5*i))

            self.logs.append(Log(LogType.SHORT, SCALED_SQUARE*5.5*i))
            self.logs.append(Log(LogType.MEDIUM, SCALED_SQUARE*6*i))

        for i in range(2):
            self.cars.append(Car(5, SCALED_SQUARE*5.5*i))
            self.logs.append(Log(LogType.LONG, SCALED_SQUARE*8.5*i))


        # create frog_home sprites
        for _ in range(5):
            self.frog_homes.append(Frog())

        # set values
        for frog in self.frog_homes:
            frog.xpos = -WINDOW_WIDTH
            frog.ypos = -WINDOW_HEIGHT

        # death animation sprites
        for _ in range(7):
            self.death_animations.append(Frog())

        # set location
        for animation in self.death_animations:
            animation.xpos = -WINDOW_WIDTH
            animation.ypos = -WINDOW_HEIGHT

    def reset(self):
        '''Resets the game'''
        self.backend.reset()
        self.player.reset()
        self.player.lives = 3

        self.turtles = []
        self.logs = []
        self.cars = []

        self.sprite_list = arcade.SpriteList()
        self.car_sprites = arcade.SpriteList()
        self.turtle_sprites = arcade.SpriteList()
        self.log_sprites = arcade.SpriteList()

        self.make_objects()
        self.load_textures()

    def check_home(self):
        '''Checks if the frog is in the home area'''
        # create 5 home center x values
        homes = [SCALED_SQUARE + (SCALED_SQUARE*3*i) for i in range(5)]
        found_home = False

        # determine if frog is home
        if self.player.ypos >= SCALED_SQUARE * 13:
            for home in homes:
                if home - SCALED_SQUARE / 2 <= self.player.xpos < home + SCALED_SQUARE / 2:
                    # add to score for reaching home
                    self.backend.points += 160
                    self.backend.points += (round(self.backend.game_time) * 10)
                    # reset max y for frog
                    self.max_frog_y = SCALED_SQUARE*1.5
                    # reset timer
                    self.backend.game_time = DURATION
                    # set frog home
                    self.frog_homes[self.frog_home_count].xpos = home
                    self.frog_homes[self.frog_home_count].ypos = SCALED_SQUARE * 13.5
                    self.frog_home_count += 1
                    found_home = True
                    # remove home from fly appearance options
                    self.fly.empty_homes_x.remove(home)
            if found_home:
                # reset frog
                self.player.reset()
            else:
                self.frog_death()

    def collision_detect(self, delta_time):
        '''Collision detection'''
        # Collision detection with cars
        if arcade.check_for_collision_with_list(self.player.sprite, self.car_sprites):
            self.frog_death()

        # determine if in water or not
        if SCALED_SQUARE * 8 < self.player.ypos < SCALED_SQUARE * 13:
            if not arcade.check_for_collision_with_lists(self.player.sprite,
                                                         (self.log_sprites, self.turtle_sprites)):
                self.frog_death()

            # Collision detection with logs
            for log in self.logs:
                if arcade.check_for_collision_with_list(self.player.sprite, log.sprite_list):
                    self.player.xpos += log.speed*delta_time*(1 + 0.15*self.backend.level)

            # Collision detection with turtles
            for turtle in self.turtles:
                collides = arcade.check_for_collision_with_list(self.player.sprite,
                                                                turtle.sprite_list)
                if collides:
                    if collides[0].texture == turtle.normal_texture:
                        self.player.xpos += turtle.speed*delta_time*(1 + 0.15*self.backend.level)
                    elif collides[0].texture == turtle.flipped_texture:
                        self.frog_death()

        # Collision detection with home frogs
        if arcade.check_for_collision_with_list(self.player.sprite, self.frog_home_sprites):
            self.frog_death()
        self.check_home()

        # Collision detection with fly
        if arcade.check_for_collision(self.player.sprite, self.fly.sprite):
            self.fly.collected = True
            self.backend.points += 200
            self.fly.set_offscreen()

    def player_score(self):
        """player points for each jump towards home"""
        # check if player moved forward past max y
        if self.player.ypos > self.max_frog_y:
            self.backend.points += 10
            self.max_frog_y = self.player.ypos

    def frog_death(self):
        """Initiates frog death, reset frog & start animation"""
        # Run death animation
        arcade.schedule(self.play_next_death_frame, 0.1)

        # Reset game state
        self.backend.game_time = DURATION
        self.player.lives -= 1

        # Cache the position before reseting the frog
        self.frog_death_x = self.player.xpos
        self.frog_death_y = self.player.ypos
        self.player.reset()

        # reset max y value of frog player through each level
        self.max_frog_y = SCALED_SQUARE * 1.5

        # reset so animation will run on every death
        self.current_animation_index = 0

    def play_next_death_frame(self, _):
        """Creates animation for when frog dies"""
        if self.current_animation_index < len(self.death_animations):
            # Show the next animation
            animation = self.death_animations[self.current_animation_index]

            # set animation positions
            animation.xpos = self.frog_death_x
            animation.ypos = self.frog_death_y

            # Reset the PREVIOUS animation to off-screen (optional, but keeps one showing at a time)
            if self.current_animation_index > 0:
                prev_animation = self.death_animations[self.current_animation_index - 1]
                prev_animation.xpos = -WINDOW_WIDTH
                prev_animation.ypos = -WINDOW_HEIGHT

            self.current_animation_index += 1
        else:
            # Reset the last animation
            last_animation = self.death_animations[-1]
            last_animation.xpos = -WINDOW_WIDTH
            last_animation.ypos = -WINDOW_HEIGHT

            # stop running death animation
            arcade.unschedule(self.play_next_death_frame)

    def flip_turtle(self, delta_time):
        """Turtle flipping"""
        self.turtle_flip_timer -= delta_time
        if self.turtle_flip_timer <= 0:
            self.turtle_flip_timer = FLIP_DELAY

            if self.turtles[0].flipped:
                self.turtles[0].flipped = False
                self.turtles[-1].flipped = True
            else:
                self.turtles[0].flipped = True
                self.turtles[-1].flipped = False

    def on_draw(self):
        if FILTER_ON:
            self.crt_filter.use()
            self.crt_filter.clear()

            self.draw_background()
            self.sprite_list.draw()
            self.death_frog_sprites.draw()
            self.backend.draw_text()

            self.window.use()
            self.clear()
            self.crt_filter.draw()
        else:
            self.window.use()
            self.clear()

            self.draw_background()
            self.sprite_list.draw()
            self.death_frog_sprites.draw()
            self.backend.draw_text()

    def on_update(self, delta_time):
        if not self.backend.paused:
            for turtle in self.turtles:
                turtle.update(delta_time, self.backend.level)
            for log in self.logs:
                log.update(delta_time, self.backend.level)
            for car in self.cars:
                car.update(delta_time, self.backend.level)
            for frog_home in self.frog_homes:
                frog_home.update()
            for animation in self.death_animations:
                animation.update()
            self.fly.update(delta_time)
            self.player.update()

            self.flip_turtle(delta_time)

            self.backend.update(delta_time)
            if self.backend.game_time <= 0:
                self.frog_death()
            self.collision_detect(delta_time)
            self.player_score()

            if self.frog_home_count >= 5:
                # reset home frogs back offscreen
                for frog in self.frog_homes:
                    frog.xpos = -WINDOW_WIDTH
                    frog.ypos = -WINDOW_HEIGHT

                # reset fly
                self.fly.level_reset()

                # reset count
                self.frog_home_count = 0

                # increment level
                self.backend.level += 1

            if self.player.lives <= 0:
                next_view = GameOverView(self.backend.points)
                self.window.show_view(next_view)

                self.backend.points = 0

    def on_key_press(self, symbol, _):
        move_keys = [arcade.key.UP, arcade.key.DOWN, arcade.key.RIGHT, arcade.key.LEFT,
                     arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]
        if symbol in move_keys:
            self.player.move(symbol)
        elif symbol == arcade.key.ESCAPE:
            arcade.close_window()
        elif symbol == arcade.key.SPACE:
            if self.backend.paused:
                self.backend.paused = False
            else:
                self.backend.paused = True

class GameOverView(arcade.View):
    """Creates the game over screen"""
    def __init__(self, score):
        super().__init__()
        self.score = score
        self.username = ""

        #path to credentials file
        script_dir = os.path.dirname(__file__)
        service_account_path = os.path.join(script_dir, "credentials.json")

        # initialize firebase
        self.db = firebase_access(service_account_path)

        # Making CRT Filter
        self.crt_filter = arcade.experimental.crt_filter.CRTFilter(FILTER_WIDTH, FILTER_HEIGHT,
                                                                   DSCALE, SCAN, PIX, WARP,
                                                                   DARKMASK, LIGHTMASK)

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK

    def on_draw(self):
        if FILTER_ON:
            self.crt_filter.use()
            self.crt_filter.clear()

            arcade.draw_text("Game Over!", WINDOW_WIDTH/2, WINDOW_HEIGHT-SCALED_SQUARE*2.5,
                             TEXT_COLOR, SCALED_SQUARE*2, anchor_x="center")
            arcade.draw_text(f"Score: {self.score}", SCALED_SQUARE*4.25,
                             WINDOW_HEIGHT/2+SCALED_SQUARE*1.5, TEXT_COLOR, SCALED_SQUARE)
            arcade.draw_text(f"Enter name: {self.username}", SCALED_SQUARE,
                             WINDOW_HEIGHT/2, TEXT_COLOR, SCALED_SQUARE)
            arcade.draw_text("Press space to play again!\n"
                             "Press enter to save score and view Leaderboard!",
                             WINDOW_WIDTH/2, SCALED_SQUARE*5, TEXT_COLOR,
                             SCALED_SQUARE, anchor_x="center", multiline=True,
                             width=WINDOW_WIDTH, align="center")

            # CRT filter applied.
            self.window.use()
            self.clear()
            self.crt_filter.draw()

        else:
            self.clear()
            arcade.draw_text("Game Over!", WINDOW_WIDTH/2, WINDOW_HEIGHT-SCALED_SQUARE*2.5,
                             TEXT_COLOR, SCALED_SQUARE*2, anchor_x="center")
            arcade.draw_text(f"Score: {self.score}", SCALED_SQUARE*4.25,
                             WINDOW_HEIGHT/2+SCALED_SQUARE*1.5, TEXT_COLOR, SCALED_SQUARE)
            arcade.draw_text(f"Enter name: {self.username}", SCALED_SQUARE,
                             WINDOW_HEIGHT/2, TEXT_COLOR, SCALED_SQUARE)
            arcade.draw_text("Press space to play again!\n"
                             "Press enter to save score and view Leaderboard!",
                             WINDOW_WIDTH/2, SCALED_SQUARE*5, TEXT_COLOR,
                             SCALED_SQUARE, anchor_x="center", multiline=True,
                             width=WINDOW_WIDTH, align="center")

    def on_key_press(self, symbol, _):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        elif symbol == arcade.key.SPACE:
            next_view = InstructionView()
            self.window.show_view(next_view)
        elif symbol == arcade.key.ENTER:
            add_entry(self.db, self.score, self.username)
            next_view = LeaderboardView(self.db)
            self.window.show_view(next_view)
        elif symbol == arcade.key.BACKSPACE:
            if len(self.username) > 0:
                self.username = self.username[:-1]
        elif arcade.key.A <= symbol <= arcade.key.Z:
            if len(self.username) < 8:
                self.username += chr(symbol)

class LeaderboardView(arcade.View):
    """Creates the leaderboard view"""
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.leaders = get_top_five(self.db)

        # Making CRT Filter
        self.crt_filter = arcade.experimental.crt_filter.CRTFilter(FILTER_WIDTH, FILTER_HEIGHT,
                                                                   DSCALE, SCAN, PIX, WARP,
                                                                   DARKMASK, LIGHTMASK)

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK

    def on_draw(self):
        if FILTER_ON:
            self.crt_filter.use()
            self.crt_filter.clear()

            arcade.draw_text("Username:     Highscore:", WINDOW_WIDTH/2,
                             WINDOW_HEIGHT-SCALED_SQUARE*2.5, TEXT_COLOR,
                             SCALED_SQUARE, anchor_x="center")
            for i, leader in enumerate(reversed(self.leaders.values())):
                arcade.draw_text(str(leader["username"]), WINDOW_WIDTH/4,
                                 WINDOW_HEIGHT - SCALED_SQUARE*(2*i + 4),
                                 TEXT_COLOR, SCALED_SQUARE, anchor_x="center")
                arcade.draw_text(str(leader["score"]), WINDOW_WIDTH*3/4,
                                 WINDOW_HEIGHT - SCALED_SQUARE*(2*i + 4),
                                 TEXT_COLOR, SCALED_SQUARE, anchor_x="center")
            arcade.draw_text("Press space bar to play!", WINDOW_WIDTH/2, SCALED_SQUARE*2.5,
                             TEXT_COLOR, SCALED_SQUARE, anchor_x="center")

            # CRT filter applied.
            self.window.use()
            self.clear()
            self.crt_filter.draw()

        else:
            self.clear()
            arcade.draw_text("Username:     Highscore:", WINDOW_WIDTH/2,
                             WINDOW_HEIGHT-SCALED_SQUARE*2.5, TEXT_COLOR,
                             SCALED_SQUARE, anchor_x="center")
            for i, leader in enumerate(self.leaders.values()):
                arcade.draw_text(str(leader["username"]), WINDOW_WIDTH/4,
                                 WINDOW_HEIGHT/4 + SCALED_SQUARE*2*i,
                                 TEXT_COLOR, SCALED_SQUARE, anchor_x="center")
                arcade.draw_text(str(leader["score"]), WINDOW_WIDTH*3/4,
                                 WINDOW_HEIGHT/4 + SCALED_SQUARE*2*i,
                                 TEXT_COLOR, SCALED_SQUARE, anchor_x="center")
            arcade.draw_text("Press space bar to play!", WINDOW_WIDTH/2, SCALED_SQUARE*2.5,
                             TEXT_COLOR, SCALED_SQUARE, anchor_x="center")

    def on_key_press(self,symbol, modifiers):
        if symbol == arcade.key.SPACE:
            next_view = InstructionView()
            self.window.show_view(next_view)
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

def main():
    """ Main function """
    # Create and setup the GameView
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Frogger")
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
