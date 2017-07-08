from .base_agent import BaseAgent

MAX_TILE_CREDIT = 10e3
MAX_DEPTH = 4
WEIGHT_MATRIX = [
    [2048, 1024, 64, 32],
    [512, 128, 16, 2],
    [256, 8, 2, 1],
    [4, 2, 1, 1]
]


class MinimaxAgent(BaseAgent):
    def get_move(self, game):
        return NotImplementedError

    def search(self, grid, alpha, beta, depth, turn, max_depth):
        return NotImplementedError

    def empty_tiles(self, game):
        return game.get_num_empty_tiles()

    def max_tile_position(self, game):
        board = game.board
        max_tile = max(max(board, key=lambda x: max(x)))

        # Considered with the WEIGHT_MATRIX, always keep the max tile in the corner
        if board[0][0] == max_tile:
            return MAX_TILE_CREDIT
        else:
            return -MAX_TILE_CREDIT

    def weighted_board(self, game):
        # TODO: try numpy matrix?
        board = game.board

        result = 0
        for i in range(len(board)):
            for j in range(len(board)):
                result += board[i][j] * WEIGHT_MATRIX[i][j]

        # Larger result means better
        return result

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

    def monotonicity(self, game):
        return NotImplementedError
