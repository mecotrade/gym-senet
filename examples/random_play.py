import time
import random

from gym_senet.envs.renderer import HumanRenderer, AnsiRenderer
from gym_senet.envs.senet import Senet, SenetGame


if __name__ == '__main__':

    board_renderer = HumanRenderer()
    ansi_renderer = AnsiRenderer()

    game = SenetGame()
    board, player = game.reset()

    print(ansi_renderer.render(board))
    board_renderer.render(board)

    time.sleep(1)

    player_wins = False
    while not player_wins:
        sticks = Senet.throw_sticks()
        print(f'player {player} throws sticks: {sticks}')

        moves = game.legal_moves(sticks)
        print(f'legal moves for player {player}: {moves}')

        random_move = random.choice(moves)
        print(f'player {player} move: {random_move}')

        board, player, player_wins, pass_turn = game.apply_move(random_move)

        print(ansi_renderer.render(board))
        board_renderer.render(board)

        if player_wins:
            print(f'player {player} wins!')
        elif pass_turn:
            print(f'turn passes to player {player}')

        time.sleep(0.2)

    board_renderer.close()
