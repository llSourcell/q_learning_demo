#!/usr/bin/python3
"""
Code  --  https://github.com/PhilippeMorere/BasicReinforcementLearning  <- old hat @2014\n
Challenge -- https://github.com/llSourcell/q_learning_demo              <- dragonWarrior teacher/student\n
Changes/commentary -- https://github.com/Ruckusist/q_learning_demo      <- Ruckusist\n

Related Material -- https://github.com/awbrown90/DeepReinforcementLearning <- tf.wizard

\n::: is this the best way to do this?

(1) solution idea... Place a bonus on the block attached to the last time this was updated,
starting from the player start, every time a new high score is reached or matched
until the optimum path is found. ::: is this better/same as a known something else?
::: does this break the rules? what are the rules?

::: is the internet fictional? Its a place people read about, but no one has ever been...
    like a good riddle poorly given.
"""


ra__author__ = 'philippe'
import World  # the other thing
import threading  # safety first!
import time

discount = 0.4 # multiplier for stuff...
actions = World.actions # list
states = [] # empty list...
Q = {} # empty set.

# create a set for all available tiles
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))

# for tile in tiles
for state in states:
    temp = {} 
    for action in actions:
        temp[action] = 0.1 # hard coded ?? 
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp

# i, j is your Q-fu, and c, w is ... c is not used and w is ...? wall?no...
for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)

# mechanicalizationism?
def do_action(action):
    s = World.player # you
    r = -World.score # -score?
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r += World.score
    #print("ran out of actions??") # completed an action
    return s, action, r, s2

# Decider of direction?
def max_Q(s):
    val = None
    act = None
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    #print("val:{}\tact:{}".format(val,act)) # what does all this mean?
    return act, val

# update cell score
def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc
    World.set_cell_score(s, a, Q[s][a])

""" MAIN Runtime functionality"""
# int main(): 
def run():
    global discount                      # self.discount
    time.sleep(1)                        # just... wait a sec
    alpha = 1                            # vs. omega being 0... i think... 
    t = 1                                # t, alpha = 1??
    high_score = 0                       # these are not the droi... i mean high score you are looking for
    #best_moves = 0                      # this should be all tupley with the high score...
    moves = 0                            # This should be used to throttle bad rounds maybe if moves > best_moves: double scoreing scheme, if moves > best_moves*2: just stop.
    games_played = 1                     # alpha, t, games_played = 1, true...
    games_to_play = 10000                # PLAY ALL NIGHT if you have to.
    max_out = 16                         # Verification of best idea... this is arbitrary
    while games_played<=games_to_play:   # this is the game loop... logic following...
        s = World.player                 # this is you... on dru... i mean this is the avatar.
        moves = t                        # reset move counter
        max_act, max_val = max_Q(s)
        #print("{}{}".format(max_act,max_val)) # max_act is the cur_act, and max_val is always .1
        (s, a, r, s2) = do_action(max_act)
        # r is the reward
        # Update Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, r + discount * max_val) # magic..

        # Check if the game has restarted
        t += 1.0
        if World.has_restarted():
            score = World.score     # self.score
            if score < high_score:  
                max_hit = 0         # reset high score hit counter
            if score > high_score:
                high_score = score  # update high score
                max_hit = 0         # and start the hit counter again... looking for 16(default)
                print("# - A new High Score has been reached:\n#\tMoves:{1}\n#\tGames Played:{2}\n#\tHigh Score:{3:.1f}".format\
                      (score,moves,games_played,high_score)) # boom
                time.sleep(1)       # self.pause for print out...
            elif score == high_score:
                max_hit +=1         # we've been down this road before
                if max_hit == max_out:
                    games_to_play = games_played; # stop up the while counter
                    print("\t########\n\tThe Game Has Ended:\n\tDistance to Target:{1}\n\tAttempts Made:{2}\n\tHigh Score:{3:.1f}\n\t########".format\
                          (score,moves,games_played,high_score)) # finish up
            time.sleep(0.01)       # self.pause for print out...
            t = 1.0               # just dont know...
            games_played += 1     # keeping track of stuff
            World.restart_game()  # AGAIN! clears my World.has_restarted() loop

        # Update the learning rate
        alpha = pow(t, -0.2) # i didnt mess with this too much...

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(0.01) # self.pace - comment out for max results
"""<endif> MAIN Runtime functionality"""

t = threading.Thread(target=run) # start a multithread process for the main()
t.daemon = True                  # is a demon
t.start()                        # Start the Thinky Part
World.start_game()               # Start the Gamey Part