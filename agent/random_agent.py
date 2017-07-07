from .base_agent import BaseAgent
from random import choice

class RandomAgent(BaseAgent):
    """A game agent pick the next move randomly."""
    def get_move(self, game):
        assert game.active_player == 'Agent'
        return self.random_move(game)