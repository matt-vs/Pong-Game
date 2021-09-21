# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals
width = 600
height = 400
ball_radius = 20
pad_width = 8
pad_height = 80
half_pad_width = pad_width / 2
half_pad_height = pad_height / 2
left = False
right = True
score1 = 0
score2 = 0
ball_pos = [width // 2, height // 2]
ball_vel = [1, -2]
# Paddles
paddle1_pos = height // 2.5
paddle2_pos = height // 2.5
paddle1_vel = 0
paddle2_vel = 0
paddle_vel = 5

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left


def spawn_ball(direction):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [width // 2, height // 2]
    if direction == right:
        ball_vel[0] = random.randrange(180, 240) / 100
        ball_vel[1] = -random.randrange(120, 200) / 100
    elif direction == left:
        ball_vel[0] = -random.randrange(180, 240) / 100
        ball_vel[1] = -random.randrange(120, 200) / 100

# define event handlers


def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2, ball_pos, ball_vel
    spawn_ball(right)
    score1 = 0
    score2 = 0
    paddle1_pos = height // 2.5
    paddle2_pos = height // 2.5


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel

    # draw mid line and gutters
    canvas.draw_line([width / 2, 0], [width / 2, height], 1, "White")
    canvas.draw_line([pad_width, 0], [pad_width, height], 1, "White")
    canvas.draw_line([width - pad_width, 0],
                     [width - pad_width, height], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # determine if ball hits gutter or hits paddle
    if ball_pos[0] - ball_radius <= pad_width:
        if paddle1_pos <= ball_pos[1] and ball_pos[1] <= paddle1_pos + pad_height:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] *= 1.10
        else:
            spawn_ball(right)
            score1 += 1

    if ball_pos[0] + ball_radius >= width - pad_width:
        if paddle2_pos <= ball_pos[1] and ball_pos[1] <= paddle2_pos + pad_height:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] *= 1.10
        else:
            spawn_ball(left)
            score2 += 1

    # Bounce off horizontal walls
    if ball_pos[1] <= ball_radius:
        ball_vel[1] = - ball_vel[1]
        ball_vel[1] *= 1.1
    elif ball_pos[1] >= height - ball_radius:
        ball_vel[1] = - ball_vel[1]
        ball_vel[1] *= 1.1

    # draw ball
    canvas.draw_circle(ball_pos, ball_radius, 10, "White", "White")

    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos >= 0 and paddle1_vel < 0) or (paddle1_pos + pad_height <= height and paddle1_vel > 0):
        paddle1_pos += paddle1_vel
    if (paddle2_pos >= 0 and paddle2_vel < 0) or (paddle2_pos + pad_height <= height and paddle2_vel > 0):
        paddle2_pos += paddle2_vel

    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos], [pad_width, paddle1_pos], [pad_width, paddle1_pos + pad_height],
                         [0, paddle1_pos + pad_height]], 1, 'White', 'White')

    canvas.draw_polygon([[width - pad_width, paddle2_pos], [width, paddle2_pos], [width, paddle2_pos + pad_height],
                         [width - pad_width, paddle2_pos + pad_height]], 1, "White", "White")

    # draw scores
    canvas.draw_text(str(score2), [width * 0.25, height * 0.25], 80, "White")
    canvas.draw_text(str(score1), [width * 0.75, height * 0.25], 80, "White")


def keydown(key):
    global paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos
    # player 1 - W and S keys
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = - paddle_vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = paddle_vel
    # player 2 Up and Down arrow
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = - paddle_vel
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = paddle_vel


def keyup(key):
    global paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos
    # player 1 W and S keys
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    # player 2 up and down arrows
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", width, height)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()
