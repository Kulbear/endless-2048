from game import Game2048
from agent import MinimaxAgent
import time

game = Game2048(game_mode=False)

m = MinimaxAgent()

start = time.time()
for i in range(1):
    step = 0
    while True:
        step += 1
        if step % 20 == 0:
            end = time.time()
            start, diff = end, end - start
            print("========== Step {} ==========".format(step))
            print("Time cost ===>", str(diff)[5] + "s")
            game.print_game()

        if game.is_lost():
            print('\n\nGame ended at step', step)
            game.print_game()
            break
        move = m.get_move(game)
        game.perform_move(move)



