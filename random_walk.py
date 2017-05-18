# !/usr/bin/python
# -*- coding: utf-8 -*-

# Authors: Ji Yang <jyang7@ualberta.ca>
# License: MIT
# Last Updated: May 18, 2017

import random
from game import Game2048


class RandomWalkAgent:
    """A 2048 game agent play with the random walk policy.

    The agent will perform a technique we defined here: Random Walk(RW).
    The result is gonna be our baseline for the entire project.
    Here, we use a special version of RW. With given probabilty,

    Parameters
    ----------
    random_prob: float
        The probability of performing a fully random move in the game.
        The float value has to be between 0 and 1, inclusively.
    task_name : str
        This string will be used as the filename of the result CSV which stores our game info

    Attributes
    ----------
    random_prob: float
        The probability of performing a fully random move in the game.
        The float value has to be between 0 and 1, inclusively.
    task_name : str
        This string will be used as the filename of the result CSV which stores our game info
    game: Game2048
        The game instance. It will be assigned with a game instance by a class method.
    """

    def __init__(self, random_prob, task_name):
        self.random_prob = random_prob
        self.task_name = task_name
        self.game = None

    def init_new_game(self):
        """Start and assign a new 2048 game instance"""
        self.game = Game2048(self.task_name)

    def play(self):
        """Perform moves on the game with our self-defined random walk policy"""
        while True:
            if random.random() < self.random_prob:
                # Fully random step
                self.game.perform_move(random.choice([0, 1, 2, 3]))
            else:
                # Move towards a selected corner
                self.game.perform_move(random.choice([0, 2]))
            # self.game.print_game()
            if self.game.end:
                score, best_tile = self.game.save_game_info()
                break


for prob in range(1, 10):
    print('Start playing with fully random probability --> {}'.format(prob / 10))
    random_walker = RandomWalkAgent(prob / 10, 'results/random_walk_prob_{}'.format(str(prob)))
    for i in range(12500):
        if i % 2500 == 0:
            print('On game #' + str(i))
        random_walker.init_new_game()
        random_walker.play()
