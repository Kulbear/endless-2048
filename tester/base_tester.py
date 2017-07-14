from game import Game2048


class BaseTester:
    def __init__(self):
        self.verbose = True
        self.result_path = ''

    def create_one_game(self):
        return Game2048(task_name=self.result_path, game_mode=False)

    def show_game_status(self, game, diff, step):
        if self.verbose:
            print('========== Step {} =========='.format(step))
            print('Time cost ===> {:.3f}s'.format(diff))
            game.print_game()

    def test_multiple_games(self, iteration=10):
        for i in range(iteration):
            self.test_one_game()

    def test_one_game(self):
        pass
