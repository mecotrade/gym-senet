import numpy as np


class Senet:

    BOARD_SIZE = 30
    HOUSE_OF_REBIRTH = 14
    HOUSE_OF_HAPPINESS = 25
    HOUSE_OF_WATER = 26
    HOUSE_OF_THREE_TRUTHS = 27
    HOUSE_OF_ISIS_AND_NEPHTHYS = 28
    HOUSE_OF_RA_HORAKHTY = 29

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
        # 1 is white side
        return np.random.choice([0, 1], 4, replace=True).tolist()

    @staticmethod
    def steps(sticks):
        white_sides = np.sum(sticks)
        return white_sides if white_sides > 0 else 5

    @staticmethod
    def legal_moves(board, player, sticks):

        protected = board[1 - player] != 0
        breaches = []
        for house in range(1, Senet.HOUSE_OF_HAPPINESS + 1):
            if protected[house-1:house+2].tolist() in [[1, 1, 1], [0, 1, 0]]:
                breaches += [house]
        protected[breaches] = 0

        num_steps = Senet.steps(sticks)

        moves = []

        #  1 - house is occupied
        # -1 - house is occupied and only this pawn can move
        available = np.where(board[player] == -1)[0]
        if not available.any():
            available = np.where(board[player] == 1)[0]

        for house in available:
            target_house = house + num_steps
            # regular piece
            if house < Senet.HOUSE_OF_HAPPINESS:
                if target_house < Senet.HOUSE_OF_HAPPINESS:
                    # no player's pieces in the target house
                    # no protected opponent's pieces (2 in a raw,
                    # but not inner in a cluster) in the target house
                    # no jumps over blockade 2 or more in a row
                    if board[player, target_house] == 0 and protected[target_house] == 0 and protected[house:target_house].sum() in [0, 1]:
                        moves += [house]
                else:
                    # Should stop at House of Happiness anyway
                    moves += [house]
            elif house == Senet.HOUSE_OF_HAPPINESS:
                # pawn which occupies House of Happiness has to make an extra move
                moves += [house]
            elif house == Senet.HOUSE_OF_WATER:
                # pawn has to make an extra move
                moves += [house]
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
        :param move: pair (house of departure, num_steps), when house of departure is Senet.BOARD_SIZE = 30,
                     this is dumb move showing that no legals moves are available and the turn passes to another player
        :return:
        """

        house, num_steps = move

        # if a pawn si mandatory, it will not be mandatory next move
        board[player, np.where(board[player] == -1)[0]] = 1

        if house == Senet.BOARD_SIZE:
            player_wins = False
            pass_turn = True
        else:
            target_house = house + num_steps
            mandatory_next = False

            # correct target house for some special cases
            if house < Senet.HOUSE_OF_HAPPINESS:
                # any pawn should stop at House of Happiness whatever num_steps is
                if target_house >= Senet.HOUSE_OF_HAPPINESS:
                    target_house = Senet.HOUSE_OF_HAPPINESS
                    mandatory_next = True
            elif house == Senet.HOUSE_OF_HAPPINESS:
                # if num_steps = 2, 3, 4 go to the target house, if it is occupied, go to House of Water
                if target_house in [Senet.HOUSE_OF_THREE_TRUTHS, Senet.HOUSE_OF_ISIS_AND_NEPHTHYS, Senet.HOUSE_OF_RA_HORAKHTY]:
                    if board[:, target_house].tolist() != [0, 0]:
                        target_house = Senet.HOUSE_OF_WATER
                    else:
                        # if target house is one of the last three, this pawn has to take move once again
                        mandatory_next = True
                # if num_steps = 1 or target house is occupied and House of Water is occupied as well,
                # go to Rebirth House
                if target_house == Senet.HOUSE_OF_WATER:
                    if board[:, target_house].tolist() != [0, 0]:
                        target_house = Senet.rebirth(board)
                    else:
                        # if target is House of Water, this pawn has to take move once again
                        mandatory_next = True
            elif house == Senet.HOUSE_OF_WATER:
                # if num_steps is 5, standby
                if num_steps == 5:
                    target_house = house
                # if num_steps is not 4, go to rebirth
                elif num_steps < 4:
                    target_house = Senet.rebirth(board)

            # move player's pawn
            board[player, house] = 0
            if target_house < Senet.BOARD_SIZE:
                board[player, target_house] = 1 if not mandatory_next else -1
                # if target house is occupied by opponent's pawn, move it to house of departure
                if board[player - 1, target_house] == 1:
                    board[player - 1, target_house] = 0
                    board[player - 1, house] = 1

            # no more pieces on the board
            player_wins = np.sum(board[player] != 0) == 0

            # pass turn if there are 2 or 3 color sides
            # keep turn if target house is one of the last three houses
            pass_turn = (num_steps in [2, 3]) and not mandatory_next

        return board, player if not pass_turn or player_wins else 1 - player, player_wins, pass_turn

    @staticmethod
    def rebirth(board):
        return Senet.HOUSE_OF_REBIRTH - (board != 0).sum(axis=0)[:Senet.HOUSE_OF_REBIRTH + 1][::-1].tolist().index(0)


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
