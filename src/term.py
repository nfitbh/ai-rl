import statistics
import time

class Term:
    def __init__(self, robot, numEpisodes, frameDuration, reportAfterEpisode) -> None:
        self.robot = robot
        self.numEpisodes = numEpisodes
        self.reportAfterEpisode = reportAfterEpisode
        self.frameDuration = frameDuration
        self.frameStartTime = time.time()

    def print_maze_visited(self, maze, episodeNum, moveHistory):
        global frameStartTime
        print(chr(27) + "[2J")
        avgCompletion = 0
        if len(moveHistory) > self.reportAfterEpisode:
            avgCompletion = statistics.mean(moveHistory[-self.reportAfterEpisode:])
        random_factor_str = "{:.1f}".format(self.robot.random_factor*100) + "%"
        st = f"Episode Number:\t\t{episodeNum}/{self.numEpisodes}\nRandom Factor:\t\t{random_factor_str}\nIts per attempt:\t{avgCompletion}\n"
        st += maze.st()
        print(st)
        delta = self.frameDuration - (time.time() - self.frameStartTime)
        #print(delta)
        if delta > 0 and delta < self.frameDuration:
            time.sleep(delta)
        self.frameStartTime = time.time()
