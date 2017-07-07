from .base_agent import BaseAgent

class MinimaxAgent(BaseAgent):
    def get_move(self, game):
        assert game.active_player == 'Agent'
        return NotImplementedError

    def empty_tiles(self, game):
        return game.get_num_empty_tiles()

    def smoothness(self, game):
        board = game.board
        smoothness = 0
        row, col = len(board), len(board[0])
        for r in board:
            for i in range(col - 1):
                smoothness += abs(r[i] - r[i + 1])
                pass
        for j in range(row):
            for k in range(col - 1):
                smoothness += abs(board[k][j] - board[k + 1][j])

        return smoothness

    def monoticity(self, game):
        return NotImplementedError
