import time
import random

from gym_senet.envs.renderer import HumanRenderer, AnsiRenderer
from gym_senet.envs.senet import Senet, SenetGame


if __name__ == '__main__':

    board_renderer = HumanRenderer()
    ansi_renderer = AnsiRenderer()

    game = SenetGame(rules='kendall')
    board, player = game.reset()

    print(ansi_renderer.render(board))
    board_renderer.render(board)

    time.sleep(1)

    done = False
    while not done:
        sticks = Senet.throw_sticks()
        print(f'player {player} throws sticks: {sticks}')

        moves = game.legal_moves(sticks)
        print(f'legal moves for player {player}: {[Senet.decode_move_for_player(move, board, player) for move in moves]}')

        random_move = random.choice(moves)
        print(f'player {player} move: {Senet.decode_move_for_player(random_move, board, player)}')

        board, player, reward, done, pass_turn = game.apply_move(random_move)

        print(ansi_renderer.render(board))
        board_renderer.render(board)

        if done:
            print(f'player {player} wins!')
        elif pass_turn:
            print(f'turn passes to player {player}')

        time.sleep(0.2)

    board_renderer.close()
