from agent import base_agent

MAX_TILE_CREDIT = 10e4
MAX_DEPTH = 1
WEIGHT_MATRIX = [
    [2048, 1024, 64, 32],
    [512, 128, 16, 2],
    [256, 8, 2, 1],
    [4, 2, 1, 1]
]

BaseAgent = base_agent.BaseAgent
AGENT = 'Agent'


class MinimaxAgent(BaseAgent):
    def get_move(self, game):
        available = game.moves_available()
        max_move = available[0] if available else None
        max_score = float('-inf')

        for d in range(1, MAX_DEPTH):
            move, score = self.search(game, float('-inf'), float('inf'), 1, d)
            if score > max_score:
                max_score = score
                max_move = move
        return max_move

    def search(self, game, alpha, beta, depth, max_depth):
        if depth > max_depth or game.is_lost():
            return self.evaluate(game)
        # Agent's turn
        if game.active_player == AGENT:
            moves = game.moves_available()
            result_move = moves[0]
            v = float('-inf')
            for m in moves:
                game_copy = game.copy()
                game_copy.perform_move(m)
                prev_v = v
                v = max(v, self.search(game_copy, alpha, beta, depth + 1, max_depth))
                if v > prev_v and depth == 1:
                    result_move = m
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            if depth == 1:
                return result_move, v
            return v
        else:
            available_tiles = game.empty_tiles()
            v = float('inf')
            for tile in available_tiles:
                game_copy = game.copy()
                # TODO: for simplicity here we only consider to fill 2
                i, j = tile
                game_copy.board[i][j] = 2
                # Switch player here
                game_copy.switch_player()
                v = min(v, self.search(game_copy, alpha, beta, depth + 1, max_depth))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            if depth == 1:
                return '', v
            return v

    def evaluate(self, game):
        empty = self.empty_tiles(game)
        position = self.max_tile_position(game)
        weighted_sum = self.weighted_board(game)
        smooth = self.smoothness(game)
        mono = self.monotonicity(game)

        # TODO: should use weights to measure heuristics
        return empty + position + weighted_sum + smooth + mono

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

        row, col = len(board), len(board[0]) if len(board) > 0 else 0
        for r in board:
            for i in range(col - 1):
                smoothness += abs(r[i] - r[i + 1])
                pass
        for j in range(row):
            for k in range(col - 1):
                smoothness += abs(board[k][j] - board[k + 1][j])

        return smoothness

    def monotonicity(self, game):
        board = game.board
        mono = 0

        row, col = len(board), len(board[0]) if len(board) > 0 else 0
        for r in board:
            diff = r[0] - r[1]
            for i in range(col - 1):
                if (r[i] - r[i + 1]) * diff <= 0:
                    mono += 1
                diff = r[i] - r[i + 1]

        for j in range(row):
            diff = board[0][j] - board[1][j]
            for k in range(col - 1):
                if (board[k][j] - board[k + 1][j]) * diff <= 0:
                    mono += 1
                diff = board[k][j] - board[k + 1][j]

        return mono
