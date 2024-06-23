from time import sleep

import numpy as np

ACTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

class Maze(object):
    def __init__(self):
        self.maze_size = (9, 9)
        self.maze = np.zeros(self.maze_size)
        #contruct the walls of the maze
        self.maze[0, 0] = 2
        self.maze[5, :5] = 1
        self.maze[:4, 5] = 1
        self.maze[2, 2:6] = 1
        self.maze[3, 2] = 1
        self.maze[1:8, 7] = 1
        self.maze[7, 2:8] = 1\
        #robot start
        self.robot_position = (0, 0)
        self.steps = 0
        self.construct_allowed_states()
        self.maze_visited = self.maze.copy()
        #used for screen shotting the maze before action begins
        #self.maze_visited[0, 0] = 0
        #print(self.st())
        #exit()

    def is_allowed_move(self, state, action):
        # check allowed move from a given state
        y, x = state
        y += ACTIONS[action][0]
        x += ACTIONS[action][1]
        if y < 0 or x < 0 or y > self.maze_size[0]-1 or x > self.maze_size[1]-1:
            # if robot will move off the board
            return False
        return (self.maze[y, x] != 1) # not a wall

    def construct_allowed_states(self):
        # create a dictionary of allowed states from any position
        # using the isAllowedMove() function
        # this is so that you don't have to call the function every time
        allowed_states = {}
        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):
                # iterate through all spaces
                #print(x, y)
                if self.maze[(y,x)] != 1:
                    # if the space is not a wall, add it to the allowed states dictionary
                    allowed_states[(y,x)] = []
                    for action in ACTIONS:
                        if self.is_allowed_move((y,x), action) & (action != 0):
                            allowed_states[(y,x)].append(action)
        self.allowed_states = allowed_states

    def update_maze(self, action):
        y, x = self.robot_position # get current position
        self.maze[y, x] = 0 # set the current position to 0
        y += ACTIONS[action][0] # get new position
        x += ACTIONS[action][1] # get new position
        self.robot_position = (y, x) # set new position
        self.maze_visited[y, x] = 2
        self.maze[y, x] = 2 # set new position
        self.steps += 1 # add steps

    def is_game_over(self):
        # check if robot in the final position
        y, x = self.robot_position
        return ((y+1, x+1) == self.maze_size)


    def get_state_and_reward(self):
        return self.robot_position, self.get_reward()

    def get_reward(self):
        # if at end give 0 reward
        # if not at end give -1 reward
        if self.robot_position == (self.maze_size[0]-1, self.maze_size[1]-1):
            return 0
        else: 
            return -1

    def st(self):
        st = "-------------------------------------------------------------------\n"
        for row in self.maze_visited:
            for col in row:
                if col == 0:
                    st += "\t" # empty space
                elif col == 1:
                    st += "X\t" # walls
                elif col == 2:
                    st += ".\t" # robot visited
            st += "\n"
        st += "-------------------------------------------------------------------\n"
        return st