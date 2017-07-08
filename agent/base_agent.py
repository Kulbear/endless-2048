from random import choice

class BaseAgent:
    def __init__(self, random_prob=0):
        self.random_prob = random_prob

    def get_move(self, game):
        pass

    def random_move(self, game):
        move = choice(game.moves_available())
        return move