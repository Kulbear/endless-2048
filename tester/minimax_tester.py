from agent import MinimaxAgent
from tester import BaseTester
import time


class MinimaxTester(BaseTester):
    """The tester for Minimax Agents.

    Parameters
    ----------
    verbose : bool
        See attributes.
    max_depth : int
        See attributes.

    Attributes
    ----------
    verbose : bool
        If True, during the agent is running, game info will be printed out.
        If False, nothing will be printed out.
    result_path : string
        Game result saving path.
    max_depth : int
        This int will be used as the maximum depth of the minimax search tree.
    """

    def __init__(self, verbose=True, max_depth=8):
        super().__init__()
        self.verbose = verbose
        self.max_depth = max_depth
        self.result_path = 'results/minimax'

    def test_one_game(self):
        """Go through one game, played by a MinimaxAgent instance"""
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
