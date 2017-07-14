from agent import MinimaxAgent
from tester import BaseTester
import time


class MinimaxTester(BaseTester):
    def __init__(self, verbose=True, max_depth=8):
        self.verbose = verbose
        self.max_depth = max_depth
        self.result_path = 'results/minimax'

    def test_one_game(self):
        game = self.create_one_game()
        m = MinimaxAgent(max_depth=self.max_depth)
        entire_start = time.time()
        start = time.time()
        step = 0
        while True:
            step += 1
            if step % 100 == 0:
                end = time.time()
                start, diff = end, end - start
                self.show_game_status(game, diff, step)

            if game.is_lost():
                print('\n\nGame ended at step {}'.format(step))
                game.print_game()
                entire_end = time.time() - entire_start
                game.save_game_info(step=step, time_cost=entire_end)
                break

            move = m.get_move(game)
            game.perform_move(move)
            game.perform_move(move)
