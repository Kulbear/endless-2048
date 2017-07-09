from game import Game2048
from agent import MinimaxAgent
import time

for i in range(100):
    game = Game2048(task_name='Minimax-D=8', game_mode=False)
    m = MinimaxAgent()
    entire_start = time.time()
    start = time.time()
    step = 0
    while True:
        step += 1
        if step % 1 == 0:
            end = time.time()
            start, diff = end, end - start
            print('========== Step {} =========='.format(step))
            print('Time cost ===>', str(diff)[:5] + 's')
            game.print_game()

        if game.is_lost():
            print('\n\nGame ended at step', step)
            game.print_game()
            entire_end = time.time() - entire_start
            game.save_game_info(step=step, time_cost=entire_end)
            break
        move = m.get_move(game)
        game.perform_move(move)
        game.perform_move(move)
