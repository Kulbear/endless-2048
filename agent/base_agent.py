from random import choice


class BaseAgent:
    """The base class of all game agents"""

    def __init__(self, random_prob=0):
        self.random_prob = random_prob

    def get_move(self, game):
        return NotImplementedError

    def random_move(self, game):
        """Pick a move from available moves randomly"""
        move = choice(game.moves_available())
        return move
