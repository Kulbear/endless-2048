from .base_agent import BaseAgent
from random import choice


class RandomAgent(BaseAgent):
    """A game agent pick the next move randomly."""

    def get_move(self, game):
        return self.random_move(game)
