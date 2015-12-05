# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = ball_vel = [0, 0]

paddle1_pos = paddle2_pos = HEIGHT/2 - PAD_HEIGHT / 2
paddle1_vel = paddle2_vel = 0

up_pressed = down_pressed = w_pressed = s_pressed = False

score1 = score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    if direction == RIGHT:
        ball_vel = [random.randrange(120, 240) / 60.0, -random.randrange(60, 180) / 60.0]
    else:
        ball_vel = [-random.randrange(120, 240) / 60.0, -random.randrange(60, 180) / 60.0]
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = score2 = 0
    if random.randint(0, 1) == 0:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[1] < BALL_RADIUS or ball_pos[1] > HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos > 0 and paddle1_vel < 0:
        paddle1_pos += paddle1_vel    
    elif paddle1_pos + PAD_HEIGHT < HEIGHT and paddle1_vel > 0:
        paddle1_pos += paddle1_vel
    if paddle2_pos > 0 and paddle2_vel < 0:
        paddle2_pos += paddle2_vel    
    elif paddle2_pos + PAD_HEIGHT < HEIGHT and paddle2_vel > 0:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_polygon([
                        (0, paddle1_pos),
                        (PAD_WIDTH, paddle1_pos),
                        (PAD_WIDTH, paddle1_pos + PAD_HEIGHT),
                        (0, paddle1_pos + PAD_HEIGHT)],
                        1, "White", "White")
    canvas.draw_polygon([
                        (WIDTH - PAD_WIDTH, paddle2_pos),
                        (WIDTH, paddle2_pos),
                        (WIDTH, paddle2_pos + PAD_HEIGHT),
                        (WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT)],
                        1, "White", "White")
    
    # determine whether paddle and ball collide
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH and paddle1_pos <= ball_pos[1] and ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
        ball_vel[0] = -1.1 * ball_vel[0]
    elif ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH) and paddle2_pos <= ball_pos[1] and ball_pos[1] <= paddle2_pos + PAD_HEIGHT:
        ball_vel[0] = -1.1 * ball_vel[0]
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        score2 += 1
        spawn_ball(RIGHT)
    elif ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH):
        score1 += 1
        spawn_ball(LEFT)
    
    # draw scores
    score1_width = frame.get_canvas_textwidth(str(score1), 32, "monospace")
    canvas.draw_text(str(score1), [WIDTH / 2 - 40 - score1_width, 60], 32, "White", "monospace")
    canvas.draw_text(str(score2), [WIDTH / 2 + 40, 60], 32, "White", "monospace")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    global up_pressed, down_pressed, w_pressed, s_pressed
    if key == simplegui.KEY_MAP["up"]:
        up_pressed = True
        paddle2_vel = -4
    if key == simplegui.KEY_MAP["down"]:
        down_pressed = True
        paddle2_vel = 4
    if key == simplegui.KEY_MAP["w"]:
        w_pressed = True
        paddle1_vel = -4
    if key == simplegui.KEY_MAP["s"]:
        s_pressed = True
        paddle1_vel = 4
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    global up_pressed, down_pressed, w_pressed, s_pressed
    if key == simplegui.KEY_MAP["up"]:
        up_pressed = False
        if not down_pressed:
            paddle2_vel = 0
        else:
            paddle2_vel = 4
    if key == simplegui.KEY_MAP["down"]:
        down_pressed = False
        if not up_pressed:
            paddle2_vel = 0
        else:
            paddle2_vel = -4
    if key == simplegui.KEY_MAP["w"]:
        w_pressed = False
        if not s_pressed:
            paddle1_vel = 0
        else:
            paddle1_vel = 4
    if key == simplegui.KEY_MAP["s"]:
        s_pressed = False
        if not w_pressed:
            paddle1_vel = 0
        else:
            paddle1_vel = -4
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)

# start frame
new_game()
frame.start()
