import time
import random

from gym_senet.envs.renderer import HumanRenderer, AnsiRenderer
from gym_senet.envs.senet import Senet


if __name__ == '__main__':

    board_renderer = HumanRenderer()
    ansi_renderer = AnsiRenderer()

    senet = Senet()
    board = senet.reset()

    print(ansi_renderer.render(board))
    board_renderer.render(board)

    time.sleep(1)

    player = Senet.CONS_PLAYER
    player_wins = False
    while not player_wins:
        sticks = senet.throw_sticks()
        print(f'player {player} throws sticks: {sticks}')

        moves = senet.legal_moves(player, sticks)
        print(f'legal moves for player {player}: {moves}')

        random_move = random.choice(moves)
        print(f'player {player} move: {random_move}')

        board, player_wins, pass_turn = senet.apply_move(player, random_move)

        print(ansi_renderer.render(board))
        board_renderer.render(board)

        if player_wins:
            print(f'player {player} wins!')
        elif pass_turn:
            player = 1 - player
            print(f'turn passes to player {player}')

        time.sleep(0.2)

    board_renderer.close()


