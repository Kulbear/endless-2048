from random import choice

class BaseAgent:
    def __init__(self, random_prob):
        self.random_prob = random_prob

    def get_move(self, game):
        pass

    def random_move(self, game):
        assert game.active_player == 'Agent'
        move = choice(game.moves_available())
        return move