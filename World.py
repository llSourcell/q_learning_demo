__author__ = 'vivek'

from Tkinter import *
import random

master = Tk()

# Aesthetics
triangle_size = 0.1
Width = 10 # pix    el width, made smaller to fit
(x, y) = (50, 50) # board dimensions, scale up or down as necessary
board = Canvas(master, width=x*Width, height=y*Width) # make the board

# Difficulty
difficulty = 2 # Higher this is, the harder the maze
walls_number = int(x * difficulty) # How many walls to generate?

# Rewards
cell_score_min = -0.2
cell_score_max = 0.2
walk_reward = -0.04

# Actions
actions = ["up", "down", "left", "right"]

# Initial conditions
def random_start():
    """Start anywhere!"""
    return(random.randrange(2,y-2), random.randrange(2,y-2)) # starting point

player = random_start()
score = 1
restart = False

# Rewards
cell_score_min = -0.2
cell_score_max = 0.2
walk_reward = -0.04

# Actions
actions = ["up", "down", "left", "right"]

# Square Functions
def create_walls(walls, x=x, y=y):
    """Let's make some walls!"""
    wall_list = [(random.randrange(4, x), random.randrange(4, y)) for i in range(0,walls)]

    if (0,0) in wall_list: # remove origin
        wall_list.remove((0,0))

    return(wall_list)

def create_reds(x=x, y=y):
    """ Lets make every other sides completely wrong to help it out"""
    wall_list = []

    wall_list += [(x-1, i, "red", -1) for i in range(0,y)] # right
    wall_list += [(0, i, "red", -1) for i in range(2,y)] # left
    wall_list += [(i, 0, "red", -1) for i in range(2,x)] # top
    wall_list += [(i, y-1, "red", -1) for i in range(0,x)] # bottom

    return(wall_list)

def create_greens():
    """ Lets make a little green corner for mercy"""
    greens = [(0, 0, "green", 1), (1, 0, "green", 1), (0, 1, "green", 1)]

    return(greens)

# Special Squares
specials = [] + create_greens() + create_reds() # x, y, color, score
walls = create_walls(walls_number) # How many random walls?
cell_scores = {}


# Board Design
def create_triangle(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)


def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            for action in actions:
                temp[action] = create_triangle(i, j, action)
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)

render_grid()


# Scoring
def set_cell_score(state, action, val):
    global cell_score_min, cell_score_max
    triangle = cell_scores[state][action]
    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255-green_dec)[2:]
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)

# Moving
def try_move(dx, dy):
    global player, x, y, score, walk_reward, me, restart

    if restart == True:
        restart_game()

    new_x = player[0] + dx
    new_y = player[1] + dy

    score += walk_reward

    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player = (new_x, new_y)
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            if score > 0:
                print "\nSuccess! | Score: ", score
            else:
                print "\n Fail! | Score: ", score
            restart = True
            return
    #print "score: ", score

# Moving
def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)

# Restarting
def restart_game():
    global player, score, me, restart
    player = random_start()
    score = 1
    restart = False
    board.coords(me, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)


def has_restarted():
    return restart

# Binding
master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="orange", width=1, tag="me")

board.grid(row=0, column=0)

# Starting
def start_game():
    master.mainloop()
