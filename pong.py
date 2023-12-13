# Pong v3.0
# Author: A1pha
"""
Classic simple game pong firstly appeared in 1972.
"""
from __future__ import annotations
from pong_variables import *
import pygame


class Ball:
    """
Creates object of class Ball, simple ball with collising with walls and objects of class Player
    """

    def __init__(self, x: int, y: int, size: int, speed: int, color: tuple):
        self.__rect = pygame.Rect((x, y), (size, size))
        self.__movement_x, self.__movement_y = [-1, 1][randint(0, 1)], [-1, 1][randint(0, 1)]
        self.__speed = speed
        self.__color = color
        self.__difficult = 0

    def check_collision(self, screen_width: int, screen_height: int, players: list[pygame.Rect]):
        """
Method of class Ball wich checks collisions between object of class Ball and walls and objects of class Player
        :param players: list of left and right player rects (pygame.Rects)
        :param screen_width: width of window with game
        :param screen_height: hegiht of window with game
        """
        if self.__rect.x <= 0 or self.__rect.x > screen_width - self.__rect.width:
            self.__rect.x, self.__rect.y = screen_width // 2, screen_height // 2
            self.__movement_x, self.__movement_y = [-1, 1][randint(0, 1)], [-1, 1][randint(0, 1)]
            self.__difficult += 0.25
        if self.__rect.y <= 5 or self.__rect.y >= screen_height - 5 - self.__rect.height:
            self.__movement_y *= -1

        left_player, right_player = players[0], players[1]
        if self.__rect.colliderect(left_player):
            if left_player.y + left_player.height // 3 <= self.__rect.y <= left_player.y + left_player.height // 3 * 2:
                self.__movement_y = 0
                self.__movement_x = 1
            if left_player.y - self.__rect.y <= self.__rect.y <= left_player.y + left_player.height // 3:
                self.__movement_y = -1
                self.__movement_x = 1
            if left_player.y + left_player.height // 3 * 2 <= self.__rect.y <= left_player.y + left_player.height:
                self.__movement_y = 1
                self.__movement_x = 1

        elif self.__rect.colliderect(right_player):
            if (right_player.y + right_player.height // 3 <= self.__rect.y <=
                    right_player.y + right_player.height // 3 * 2):
                self.__movement_y = 0
                self.__movement_x = -1
            if right_player.y - self.__rect.y <= self.__rect.y <= right_player.y + right_player.height // 3:
                self.__movement_y = -1
                self.__movement_x = -1
            if right_player.y + right_player.height // 3 * 2 <= self.__rect.y <= right_player.y + right_player.height:
                self.__movement_y = 1
                self.__movement_x = -1

    def move(self):
        """
Method of class Ball which moves object of class Ball in a direction, depends on x, y flags
        """
        self.__rect.x += self.__movement_x * (self.__speed + self.__difficult)
        self.__rect.y += self.__movement_y * (self.__speed + self.__difficult)

    def draw(self, screen: pygame.Surface):
        """
Method of class Ball which draws object of class Ball on a surface, giving as a parameter
        :param screen: surface, where object of class Ball would be drowned
        """
        pygame.draw.rect(screen, self.__color, self.__rect)

    def get_rect(self) -> pygame.Rect:
        """
Method of class Ball which returns copy rect (pygame.Rect) of object of class Ball
        :return: copy rect (pygame.Rect) of object of class Ball
        """
        return self.__rect.copy()


class Player:
    """
Creates an object of class Player. Players in pong are placed on both sides of the screen and colises
with ball and walls.
    """
    def __init__(self, x: int, y: int, width: int, height: int, speed: int, color: tuple, left=False, right=False):
        self.__rect = pygame.Rect((x, y), (width, height))
        self.__left, self.__right = left, right
        self.__directions = {
            pygame.K_w: False, pygame.K_s: False, pygame.K_UP: False, pygame.K_DOWN: False
        }
        self.__speed = speed
        self.__color = color

    def check_collision(self, screen_height: int):
        """
Method of class Player which checks collisions between object of class Player and walls
        :param screen_height: height of window with game
        """
        if self.__rect.y < 5:
            self.__rect.y = 5
        if self.__rect.y > screen_height - 5 - self.__rect.height:
            self.__rect.y = screen_height - self.__rect.height - 5

    def get_direction_keys(self):
        return self.__directions.keys()

    def check_events(self, event: pygame.event):
        """
Method of class Player which checks inpput events (from keyboard) and changes player's direction the following way:
to bottom (S for left player, KEY DOWN for right player) / to top (W for left player, KEY UP for right player)
        :param event: event (from keyboard) received from method of class Game
        """
        if event.type == pygame.KEYDOWN:
            self.__directions[event.key] = True
        if event.type == pygame.KEYUP:
            self.__directions[event.key] = False

    def move(self):
        """
Method of class Player which moves object of class Player in to top or to bottom, depends on y flag,
aslo oject can stop.
        """
        self.__rect.y += self.__speed * (
                (self.__directions[pygame.K_s] - self.__directions[pygame.K_w]) * self.__left +
                (self.__directions[pygame.K_DOWN] - self.__directions[pygame.K_UP]) * self.__right
        )

    def draw(self, screen: pygame.Surface):
        """
Method of class Player which draws object of class Player on a surface, giving as a parameter
        :param screen: surface, where object of class Player would be drowned
        """
        pygame.draw.rect(screen, self.__color, self.__rect)

    def get_rect(self) -> pygame.Rect:
        """
Method of class Player which returns copy rect (pygame.Rect) of object of class Player
        :return: copy rect (pygame.Rect) of object of class Player
        """
        return self.__rect.copy()


class Counter:
    """
Creates an object of class Counter. Both sides have counter so wins that side which has more points on counter.
    """

    def __init__(self, x: int, y: int, size: int, count: int, digits: list, left=False, right=False):
        self.__rect_tens = pygame.Rect((x, y), (size, size))
        self.__rect_ones = pygame.Rect((x + size, y), (size, size))
        self.__count = count
        self.__left, self.__right = left, right
        self.__digits = digits

    def add_score(self, ball, screen_width: int):
        """
Method of class Counter which adds point to the side which scored a goal to another.
        :param ball: list or tuple, containing info: [object_x, object_size]
        :param screen_width: width of window with game
        """

        if ball.x <= 0 and self.__right:
            self.__count += 1
        if ball.x > screen_width - ball.width and self.__left:
            self.__count += 1

    def check_winner(self) -> tuple[bool, bool] | bool:
        """
Method of class Counter which returns amount od scores
        :return: integer equals to amount of scores
        """
        if self.__count == 20:
            return self.__left, self.__right
        else:
            return False

    def get_count(self) -> int:
        """
Mehtod of class Counter which returns current amount of points
        :return: current amount of points
        """
        return self.__count

    def draw(self, screen: pygame.Surface):
        """
Method of class Counter which draws object of class Counter on a surface, giving as a parameter
        :param screen: surface, where object of class Counter would be drowned
        """
        screen.blit(self.__digits[self.__count // 10], self.__rect_tens)
        screen.blit(self.__digits[self.__count % 10], self.__rect_ones)


class Game:
    """
Main class. Creates an object of class Game. Contains and proccess all previous classes.
    """

    def __init__(self, width: int, height: int, game_FPS: int):
        pygame.init()

        self.__screen_width, self.__screen_height = width, height
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height), pygame.FULLSCREEN)

        self.__FPS = game_FPS
        self.__clock = pygame.time.Clock()

        self.__game_end = False

        self.__background = pygame.transform.smoothscale(
            pygame.image.load('images/background.png').convert_alpha(),
            (self.__screen_width, self.__screen_height)
        )

        self.__digits = list()
        for i in range(10):
            digit = pygame.image.load(f'images/digits/{i}.png')
            digit.set_colorkey((0, 0, 0))
            self.__digits.append(
                pygame.transform.smoothscale(
                    digit.convert_alpha(),
                    (counter_size, counter_size)
                )
            )

        self.__victory_sound = pygame.mixer.Sound('sounds/victory_sJDDywi.wav')

        self.__players = list()
        self.__players.append(
            Player(
                start_left_player_x, start_left_player_y, player_width, player_height, player_speed, WHITE, True
            )
        )
        self.__players.append(
            Player(
                start_right_player_x, start_right_player_y, player_width, player_height, player_speed, WHITE, right=True
            )
        )

        self.__ball = Ball(
            start_ball_x, start_ball_y, ball_size, start_ball_speed, GRAY
        )

        self.__counters = list()
        self.__counters.append(
            Counter(left_player_counter_x, left_player_counter_y, counter_size, 0, self.__digits, True)
        )
        self.__counters.append(
            Counter(right_player_counter_x, right_player_counter_y, counter_size, 0, self.__digits, right=True)
        )

    def __del__(self):
        """
Standart method of class, which closes pygame and shows winner if it is
        """
        if self.__game_end:
            if self.__counters[0].get_count() > self.__counters[1].get_count():
                self.__screen.blit(
                    pygame.transform.smoothscale(
                        pygame.image.load('images/left_player_won.png').convert_alpha(),
                        (self.__screen_width, self.__screen_height)
                    ), (0, 0)
                )
            elif self.__counters[0].get_count() < self.__counters[1].get_count():
                self.__screen.blit(pygame.transform.smoothscale(
                    pygame.image.load('images/right_player_won.png').convert_alpha(),
                    (self.__screen_width, self.__screen_height)
                    ), (0, 0)
                )
            else:
                self.__screen.blit(pygame.transform.smoothscale(
                    pygame.image.load('images/draw.png').convert_alpha(),
                    (self.__screen_width, self.__screen_height)
                    ), (0, 0)
                )

            self.__victory_sound.play()

            pygame.display.flip()
            pygame.time.wait(5000)
        pygame.quit()

    def run(self):
        """
Main method of class Game, contains logic, movement and drawing proccesses.
        """
        while not self.__game_end:
            self.__screen.blit(self.__background, (0, 0))
            self.__check_events()
            self.__game_move()
            self.__game_logic()
            self.__game_draw()

            pygame.display.flip()
            self.__clock.tick(self.__FPS)

    def __check_events(self):
        """
Method of class game which checks events on closing game and also check events for class Player objects'
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_end = True
            for player in self.__players:
                if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                    if event.key in player.get_direction_keys():
                        player.check_events(event)

    def __game_logic(self):
        """
Mehtod of class Game which process logic of game (ball's logic, objects' of class Player logis and objects'
of class Counter)
        """
        for counter in self.__counters:
            counter.add_score(self.__ball.get_rect(), self.__screen_width)
            if counter.check_winner():
                self.__game_end = True

        self.__ball.check_collision(
            self.__screen_width, self.__screen_height, [
                player.get_rect() for player in self.__players
            ]
        )

        for player in self.__players:
            player.check_collision(self.__screen_height)

    def __game_move(self):
        """
Method of class Game which changes positional args (such as x, y) for all moving elements of game
        """
        self.__ball.move()
        for player in self.__players:
            player.move()

    def __game_draw(self):
        """
Method of class Game which show all elements of game on screen
        """
        self.__ball.draw(self.__screen)

        for player in self.__players:
            player.draw(self.__screen)

        for counter in self.__counters:
            counter.draw(self.__screen)


def main():
    """
Main part of code. Initializates pong.
    """
    pygame.display.set_caption('Pong')
    game = Game(screen_width_workpiece, screen_height_workpiece, FPS)
    game.run()


if __name__ == '__main__':
    main()
