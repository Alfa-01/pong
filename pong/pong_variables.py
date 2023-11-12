"""
Module which contains auxiliary valuables for main code.
"""

from random import randint

# Screen's settings
screen_width_workpiece = 1920
screen_height_workpiece = 1080

# Player's settings
player_width = 20
player_height = 150
start_left_player_x = 10
start_left_player_y = 300
start_right_player_x = screen_width_workpiece - start_left_player_x - player_width
start_right_player_y = screen_height_workpiece - start_left_player_y
player_speed = 10

# Ball's settings
ball_size = 15
start_ball_x, start_ball_y = screen_width_workpiece // 2, screen_height_workpiece // 2
start_ball_speed = 10
start_ball_movement_x = [-1, 1][randint(0, 1)]
start_ball_movement_y = [-1, 1][randint(0, 1)]

# Counter's settings
counter_size = 100
left_player_counter_x = screen_width_workpiece // 2 - 2 * counter_size - 5
right_player_counter_x = screen_width_workpiece // 2 - 5
left_player_counter_y = right_player_counter_y = 16

# FPS's settings
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
