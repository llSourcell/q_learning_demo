__author__ = 'vivek'

import World
import threading
import time

import random

# Initial Values
discount = 0.3 # discount
actions = World.actions # actions
states = [] # states
Q = {} # policies / rewards

# Define World
for i in range(World.x):
    """ Loads all available states (squares) in the World"""
    for j in range(World.y):
        states.append((i, j))

for state in states:
    """ For every state, set the default reward for each action to 0.1"""
    temp = {}
    for action in actions:
        temp[action] = 0.1
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp

for (i, j, c, w) in World.specials:
    """ For x, y, color, score in each World.specials list, update the Q reward array so reaching this square through any action earns the new reward"""
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)

# Value Functions
def max_Q(s):
    """ For current position, check which of the next available squares provide the highest Q value. If more than one, choose randomly.

    input:
    s: current position
    epsilon: value of random actions

    output:
    best_a : best action
    best_q: best q value for that action"""

    best_q = None
    best_a = None

    for a, q in Q[s].items(): # for every action and q value
        if best_q is None or (q > best_q): # if val is 0 or current q is higher, assign current a, q
            #print('Checking for an Action...')

            best_q = q
            best_a = a

    options = [x for x in Q[s].items() if x[1] == best_q] # How many options do we have?

    if len(options) > 1:
        # If more than option, pick the best one
        best_a, best_q = options[random.randrange(0,len(options))]

    if best_q < 0.1:
        # If all the options are bad (less than the regular reward) do something random!
        best_a, best_q = Q[s].items()[random.randrange(0,len(Q[s].items()))]

    return best_a, best_q



def inc_Q(s, a, alpha, inc):
    """ Given the position, action, the learning rate, and inc, set the new cell score.

    We use the alpha to decrease the value of moves over time; the longer a new policy takes, the less its Q value becomes in the q matrix.

    s: current position
    a: current action
    alpha: current learning rate
    inc: r + discount * max_val (World Score + Discount * MaxQ(s).val)
    """

    # For the specific action
    Q[s][a] *= 1 - alpha # multiply the Q value for an action by the learning rate
    Q[s][a] += alpha * inc # add the incoming value of the alpha * action

    World.set_cell_score(s, a, Q[s][a]) # Set the score of getting to the current position using the action to the new Q[s][a]

# Moving Functions
def do_action(action):
    """
    Given an action, make an actual move in the real world.

    s = current player position
    r = the current score increased by the cost/reward of the next action
    s2 = updated player position
    """
    s = World.player
    r = -World.score

    if action == actions[0]:
        # down
        World.try_move(0, -1)

    elif action == actions[2]:
        # left
        World.try_move(-1, 0)

    elif action == actions[1]:
        # up
        World.try_move(0, 1)

    elif action == actions[3]:
        # right
        World.try_move(1, 0)
    else:
        return

    s2 = World.player
    r += World.score
    return s, action, r, s2


# Start Game
def run():
    global discount
    time.sleep(1)

    alpha = 1
    beta = None

    t = 1

    stuck = 0
    old_s = (0,0)

    while True:
        s = World.player # Starting Position

        if s == old_s: # Stuck Check
            stuck += 1
            #print('Been in the same spot this many times:{}'.format(stuck))

        # Before Move
        # Current Position
        #print('Current Position: {},\n Potential Actions: {}\n\n'.format(s, Q[s]))

        # Potential Actions
        max_act, max_val = max_Q(s) # find the next highest Q from position s
        #print('Suggested Action: {},\n Q Value: {}\n\n'.format(max_act, max_val))

        # Making Move
        (s, a, r, s2) = do_action(max_act) # Return the results of an action from old s to new s2
        #print('New Position: {},\n Current Score: {},\n Actual Move: {},\n Old Position {}\n\n'.format(s2, r, a, s2))

        # Learning Consequences
        # alpha: learning rate; cost of taking too many moves, if the alpha grows too quickly, bad moves seem less bad over time. (Really is a 'learning rate'; measures consequence of actions)
        # beta: summary of the reward function, which takes the world score, discount, and best q to update the value of that action

        epsilon = pow(t, -0.005)
        alpha = pow(t, -0.25)
        beta =  r + discount * max_val

        # Check Values at New Position
        max_act, max_val = max_Q(s2) # return the score at s2
        #print('Suggested Action at New Position: {},\nQ Value at New Position: {}\n'.format(max_act, max_val)) # seems to be the same position. Hmm....

        # Update Q Matrix
        inc_Q(s, a, alpha, beta)
        #print('Updating Q value at Position: {},\n for Action: {}, \n with Alpha {},\n and Beta {}\n'.format(s, a, alpha, beta, max_val))

        t += 1.0
        old_s = s

        print('Moves {} | Score {}'.format(t, round(World.score, 2)))


        if World.has_restarted() or (t > 100) or (stuck > 10): # 500 tries per life, or you get stuck more than 10 times
            World.restart_game()
            time.sleep(0.01)

            t = 1.0
            stuck = 0


        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(0.01) # seconds between moves
        # sanic


t = threading.Thread(target=run)
t.daemon = True
t.start()

World.start_game()
