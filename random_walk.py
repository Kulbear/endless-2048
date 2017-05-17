# !/usr/bin/python
# -*- coding: utf-8 -*-

# Authors: Ji Yang <jyang7@ualberta.ca>
# License: MIT
# Last Updated: May 17, 2017

import random
from game import Game2048


class RandomWalk:
    def __init__(self, prob_random, task_name):
        self.prob_random = prob_random
        self.task_name = task_name
        self.game = None

    def init_new_game(self):
        self.game = Game2048(self.task_name)

    def play(self, step_num):
        i = 0
        while i < step_num:
            i += 1
            if random.random() < self.prob:
                self.game.perform_move(random.choice([0, 1, 2, 3]))
            else:
                self.game.perform_move(random.choice([0, 2]))
            # self.game.beautiful_print()
            if self.game.end:
                score, best_tile = self.game.save_game_info()
                break


for prob in range(0, 10):
    print('With full random prob: {}'.format(prob / 10))
    my_exp = RandomWalk(prob / 10, 'random_walk_prob_{}'.format(str(prob)))
    for i in range(20000):
        my_exp.init_new_game()
        my_exp.play(1000)
