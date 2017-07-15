from tester import MinimaxTester

if __name__ == '__main__':
    # Just for demo
    testers = [
        MinimaxTester(max_depth=8, verbose=True)
        # Add other testers here
    ]

    for tester in testers:
        # tester.test_one_game()
        tester.test_games(iteration=10)
