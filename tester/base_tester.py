from game import Game2048


class BaseTester:
    """The base tester class for all testers.

    Attributes
    ----------
    verbose : bool
        If True, during the agent is running, game info will be printed out.
        If False, nothing will be printed out.
    result_path : string
        Game result saving path.
    """

    def __init__(self):
        self.verbose = True
        self.result_path = ''

    def create_one_game(self):
        """Generate a new game instance"""
        return Game2048(task_name=self.result_path, game_mode=False)

    def show_game_status(self, game, diff, step):
        """In Verbose mode, print out the current game information"""
        if self.verbose:
            print('========== Step {} =========='.format(step))
            print('Time cost ===> {:.3f}s'.format(diff))
            game.print_game()

    def test_multiple_games(self, iteration=10):
        """Run the game multiple times"""
        # TODO: multithread?
        for i in range(iteration):
            self.test_one_game()

    def test_one_game(self):
        return NotImplementedError
