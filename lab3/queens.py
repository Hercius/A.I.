import time
import random
import numpy as np
import math

class Board(object):
    """An N-queens candidate solution ."""

    def __init__(self,N):
        """A random N-queens instance"""
        self.queens = dict()
        for col in range(N):
            row = random.choice(range(N))
            self.queens[col] = row

    def copy(self,board):
        """Copy a board (prevent aliasing)"""
        self.queens = board.queens.copy()
        
    def actions(self):
        """Return a list of possible actions given the current placements."""
        # YOU FILL THIS IN
        possibleActions = []
        
        for queen in range(len(self.queens)):
            for possibleAction in range(len(self.queens)):
               if self.queens[queen] != possibleAction: 
                possible = []
                possible.append(queen)
                possible.append(possibleAction)
                possibleActions.append(possible)
        return possibleActions
                    
        

    def neighbor(self, action):
        """Return a Board instance like this one but with one action made."""
        self.queens[action[0]] = action[1]
        return self
        
    def cost(self):
        """Compute the cost of this solution."""
        # YOU FILL THIS IN
        cost = 0
        for queen in range(len(self.queens)):
            for nextQueen in range (queen+1, len(self.queens)):
                if self.queens[queen] == self.queens[nextQueen] or abs(queen - nextQueen) == abs(self.queens[queen] - self.queens[nextQueen]):
                    cost += 1
        return cost 


cooling_schedule = {'none': lambda T0,t: T0,
                    'linear': lambda T0,t: T0/(1+t),
                    'logarithmic': lambda T0,t: T0/math.log(1+t)}


def simulated_annealing(env):

    ## set start temperature
    starttemp = int(env.starttemp.get())

    ## set temperature schedule
    temp = cooling_schedule[env.coolmode.get()]

    ## set search cutoff
    maxsteps = int(env.control.params.maxsteps.get())

    
    ## Initial random board
    x = Board(8);
    T0 = starttemp
    steps = 1
    env.solved = False
    while x.cost() > 0 and steps < maxsteps and env.alive and env.running:
        randomAction = random.choice(x.actions())
        possibleMove = x.neighbor(randomAction)
        if possibleMove.cost() < x.cost():
            x = possibleMove
        else:
            heatup = possibleMove.cost() - x.cost()
            probability = np.exp(-heatup/temp(T0,steps))
            if probability > random.random():
                x = possibleMove
        if (steps % 100 == 0):
            env.display(x)
            env.message('SIMULATED ANNEALING\nstep {}\ntemperature: {:.5e}\ncost: {}'.format(steps,temp(T0,steps),x.cost()))
            time.sleep(0.1)
        steps = steps+1

    env.display(x);
    env.message('SIMULATED ANNEALING\nstep {}\ntemperature: {:.5e}\ncost: {}'.format(steps,temp(T0,steps),x.cost()))
    if x.cost == 0: env.solved = True
    return steps

