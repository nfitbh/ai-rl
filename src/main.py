import time

import numpy as np
from environment import Maze
from agent import Agent
from term import Term


import statistics


frameStartTime = time.time()
frameDuration = 0.05



if __name__ == '__main__':
    num_episodes = 4000
    reportAfterEpisodes = 5
    maze = Maze()
    robot = Agent(maze.maze, alpha=0.1, random_factor=1.0, random_adjust=-0.00027, min_random_factor=0.0)
    term = Term(robot, num_episodes, frameDuration, reportAfterEpisodes)
    moveHistory = []

    for i in range(num_episodes):
       
        while not maze.is_game_over():
            state, _ = maze.get_state_and_reward() # get the current state
            action = robot.choose_action(state, maze.allowed_states[state]) # choose an action (explore or exploit)
            maze.update_maze(action) # update the maze according to the action
            state, reward = maze.get_state_and_reward() # get the new state and reward
            robot.update_state_history(state, reward) # update the robot memory with state and reward
            
            if maze.steps > 10000:
                break
       
        robot.learn() # robot should learn after every episode
        robot.update_random_factor()
        moveHistory.append(maze.steps) # get a history of number of steps taken to plot later

        if i % reportAfterEpisodes == 0:
            term.print_maze_visited(maze, i, moveHistory)
        if i < num_episodes-1:
            maze = Maze() # reinitialize the maze
    term.print_maze_visited(maze, i+1, moveHistory)
    