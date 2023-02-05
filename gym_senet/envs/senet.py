import numpy as np


class Senet:

    BOARD_SIZE = 30
    HOUSE_OF_REBIRTH = 14
    HOUSE_OF_HAPPINESS = 25
    HOUSE_OF_WATER = 26
    HOUSE_OF_THREE_TRUTHS = 27
    HOUSE_OF_RE_ATOUM = 28

    CONS_PLAYER = 0
    SPOOLS_PLAYER = 1

    @staticmethod
    def empty_board():
        return np.zeros([2, Senet.BOARD_SIZE], dtype=int)

    @staticmethod
    def init_board(num_pieces):
        board = Senet.empty_board()
        board[Senet.CONS_PLAYER, 0:2*num_pieces:2] = 1
        board[Senet.SPOOLS_PLAYER, 1:2*num_pieces+1:2] = 1
        return board

    @staticmethod
    def throw_sticks():
        # 0 is black side
        # 1 is color side
        return np.random.choice([0, 1], 4, replace=True).tolist()

    @staticmethod
    def steps(sticks):
        color_sides = np.sum(sticks)
        return color_sides if color_sides > 0 else 5

    @staticmethod
    def legal_moves(board, player, sticks):

        protected = board[1 - player].copy()
        count = 0
        for house in range(Senet.HOUSE_OF_WATER):
            if protected[house] == 0:
                count = 0
            else:
                count += 1
                protected[house] = count
        for house in reversed(range(Senet.HOUSE_OF_WATER)):
            if protected[house] == 0:
                count = 0
            else:
                count = max(count, protected[house])
                protected[house] = count

        num_steps = Senet.steps(sticks)

        moves = []

        for house in np.where(board[player] == 1)[0]:
            target_house = house + num_steps
            # regular piece
            if house < Senet.HOUSE_OF_HAPPINESS:
                if target_house < Senet.HOUSE_OF_HAPPINESS:
                    # no player's pieces in the target house
                    # no protected another player's pieces (2 or more in a row) in the target house
                    # no jumps over blockade 3 or more in a row
                    if board[player, target_house] == 0 and protected[target_house] < 2 and protected[house:target_house].max() < 3:
                        moves += [house]
                elif target_house == Senet.HOUSE_OF_HAPPINESS:
                    # House of Happiness is empty
                    if board[:, target_house].sum() == 0:
                        moves += [house]
            # happy piece
            elif house == Senet.HOUSE_OF_HAPPINESS:
                # remove or target house is empty
                if target_house == Senet.BOARD_SIZE or board[:, target_house].sum() == 0:
                    moves += [house]
            elif house == Senet.HOUSE_OF_WATER:
                # can't be
                raise Exception(f'Something went wrong, player {player} piece is in the Water House')
            elif house > Senet.HOUSE_OF_WATER:
                # remove only
                if target_house == Senet.BOARD_SIZE:
                    moves += [house]

        return [(h, num_steps) for h in moves] if moves else [(Senet.BOARD_SIZE, 0)]

    @staticmethod
    def apply_move(board, player, move):
        """
        :param board:
        :param player:
        :param move: pair (house of depart, num_steps), when house of depart is Senet.BOARD_SIZE = 30,
                     this is dumb action showing that no legals moves available and the move passes to another player
        :return:
        """

        house, num_steps = move

        if house == Senet.BOARD_SIZE:
            player_wins = False
            pass_turn = True
        else:
            target_house = house + num_steps

            board[player, house] = 0

            if target_house < Senet.BOARD_SIZE and target_house != Senet.HOUSE_OF_WATER:
                board[player, target_house] = 1
                # if move is legal and target house is occupied another
                if target_house < Senet.HOUSE_OF_HAPPINESS and board[1 - player, target_house] == 1:
                    board[1 - player, target_house] = 0
                    board[1 - player, house] = 1
            elif target_house == Senet.HOUSE_OF_WATER:
                # rebirth in the House of Rebirth or closest empty house before it
                rebirth = Senet.HOUSE_OF_REBIRTH - board.sum(axis=0)[:Senet.HOUSE_OF_REBIRTH + 1][::-1].tolist().index(0)
                board[player, rebirth] = 1

            # no more pieces on the board
            player_wins = np.sum(board[player]) == 0

            # pass turn if there are 2 or 3 color sides
            # keep turn if target house is one of the last three houses
            pass_turn = (num_steps in [2, 3]) and (target_house not in [Senet.HOUSE_OF_THREE_TRUTHS,
                                                                        Senet.HOUSE_OF_RE_ATOUM,
                                                                        Senet.BOARD_SIZE - 1])

        return board, player if not pass_turn else 1 - player, player_wins, pass_turn


class SenetGame:

    def __init__(self, num_pieces=5):

        self.num_pieces = num_pieces
        self.board = np.empty([2, Senet.BOARD_SIZE], dtype=int)
        self.player = None

        self.reset()

    def reset(self):
        self.board = Senet.init_board(self.num_pieces)
        self.player = Senet.CONS_PLAYER
        return self.board, self.player

    def legal_moves(self, sticks):
        return Senet.legal_moves(self.board, self.player, sticks)

    def apply_move(self, move):
        board, player, player_wins, pass_turn = Senet.apply_move(self.board, self.player, move)
        self.player = player
        return board, player, player_wins, pass_turn
