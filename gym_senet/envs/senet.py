import numpy as np


class Senet:

    BOARD_SIZE = 30
    HOUSE_OF_REBIRTH = 14
    HOUSE_OF_HAPPINESS = 25
    HOUSE_OF_WATER = 26
    HOUSE_OF_THREE_TRUTHS = 27
    HOUSE_OF_RE_ATUM = 28
    HOUSE_OF_RE_HORAKHTY = 29

    CONS_PLAYER = 0
    SPOOLS_PLAYER = 1

    INNER_DANCER = 42
    SAFE_DANCER = 43
    NO_DANCER = -1
    PASS_TURN = 0

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
        # 1 is colored side
        return np.random.choice([0, 1], 4, replace=True).tolist()

    @staticmethod
    def steps(sticks):
        colored_sides = np.sum(sticks)
        return colored_sides if colored_sides > 0 else 5

    @staticmethod
    def roll_dice():
        return np.random.randint(1, 6)

    @staticmethod
    def detect_clusters(board, player):

        clusters = board[1 - player].copy()

        cluster_first = 0 if clusters[0] != 0 else -1
        cluster_size = 1 if cluster_first != -1 else 0
        for house in range(1, Senet.HOUSE_OF_WATER + 1):
            if clusters[house] != 0:
                if cluster_first == -1:
                    cluster_first = house
                    cluster_size = 1
                else:
                    cluster_size += 1
            else:
                if cluster_first != -1:
                    clusters[cluster_first] = cluster_size
                    clusters[house - 1] = cluster_size
                    clusters[cluster_first+1:house-1] = Senet.INNER_DANCER
                    cluster_first = -1

        # House of Rebirth is always protected
        if clusters[Senet.HOUSE_OF_REBIRTH] == 1:
            clusters[Senet.HOUSE_OF_REBIRTH] = Senet.SAFE_DANCER

        return clusters

    @staticmethod
    def encode_move(dancer_id, num_steps):
        return Senet.PASS_TURN if dancer_id == Senet.NO_DANCER else dancer_id * 10 + (num_steps if num_steps > 0 else (11 + num_steps))

    @staticmethod
    def decode_move(move):
        if move == Senet.PASS_TURN:
            return Senet.NO_DANCER, 0
        else:
            move -= 1
            dancer_id, num_steps = move // 10, move % 10
            num_steps = num_steps + 1 if num_steps < 5 else (num_steps - 10)
            return dancer_id, num_steps

    @staticmethod
    def decode_move_for_player(move, board, player):
        dancer_id, num_steps = Senet.decode_move(move)
        return np.where(board[player] == 1)[0][dancer_id] if dancer_id != Senet.NO_DANCER else Senet.NO_DANCER, num_steps


class SenetKendall(Senet):

    @staticmethod
    def legal_moves(board, player, num_steps):

        clusters = SenetKendall.detect_clusters(board, player)

        moves = []
        dancers = np.where(board[player] == 1)[0]
        for dancer_id, dancer in enumerate(dancers):
            landing_house = dancer + num_steps
            # regular piece
            if dancer < Senet.HOUSE_OF_HAPPINESS:
                if landing_house < Senet.HOUSE_OF_HAPPINESS:
                    # no player's dancer in the target house
                    # no protected another dancer's pieces in the target house:
                    # 2 in a row and House of Rebirth
                    # no jumps over blockade: 3 or more in a row
                    if (board[player, landing_house] == 0
                            and clusters[landing_house] in [0, 1]
                            and clusters[dancer:landing_house].max(initial=0) != SenetKendall.INNER_DANCER):
                        moves += [Senet.encode_move(dancer_id, num_steps)]
                elif landing_house == Senet.HOUSE_OF_HAPPINESS:
                    # House of Happiness is empty
                    if (board[:, landing_house].sum() == 0
                            and clusters[landing_house] in [0, 1]
                            and clusters[dancer:landing_house].max(initial=0) != SenetKendall.INNER_DANCER):
                        moves += [Senet.encode_move(dancer_id, num_steps)]
            # happy piece
            elif dancer == Senet.HOUSE_OF_HAPPINESS:
                # remove or target house is empty
                if landing_house == Senet.BOARD_SIZE or board[:, landing_house].sum() == 0:
                    moves += [Senet.encode_move(dancer_id, num_steps)]
            elif dancer == Senet.HOUSE_OF_WATER:
                # can't be
                raise Exception(f'Something went wrong, player {player} piece is in the House of Water')
            elif dancer > Senet.HOUSE_OF_WATER:
                # remove only
                if landing_house == Senet.BOARD_SIZE:
                    moves += [Senet.encode_move(dancer_id, num_steps)]

        # backward moves when no forward moves are available
        # only for regular houses
        if not moves:
            for dancer_id, dancer in enumerate(dancers):
                if dancer < Senet.HOUSE_OF_HAPPINESS:
                    landing_house = dancer - num_steps
                    if (landing_house >= 0
                            and board[player, landing_house] == 0
                            and clusters[landing_house] in [0, 1]
                            and clusters[landing_house:dancer].max(initial=0) != SenetKendall.INNER_DANCER):
                        moves += [Senet.encode_move(dancer_id, -num_steps)]

        # if still no moves are available, add pass turn
        return moves if moves else [Senet.PASS_TURN]

    @staticmethod
    def apply_move(board, player, move):
        """
        :param board:
        :param player:
        :param move: 0 for pass turn, otherwise move encoded to an integer
        :return:
        """

        if move == Senet.PASS_TURN:
            reward = 0
            done = False
            pass_turn = True
        else:
            dancers = np.where(board[player] == 1)[0]
            dancer_id, num_steps = SenetKendall.decode_move(move)

            house = dancers[dancer_id]
            landing_house = house + num_steps

            board[player, house] = 0

            if landing_house < Senet.BOARD_SIZE and landing_house != Senet.HOUSE_OF_WATER:
                board[player, landing_house] = 1
                # if move is legal and target house is occupied another
                if landing_house < Senet.HOUSE_OF_HAPPINESS and board[1 - player, landing_house] == 1:
                    board[1 - player, landing_house] = 0
                    board[1 - player, house] = 1
            elif landing_house == Senet.HOUSE_OF_WATER:
                # rebirth in the House of Rebirth or closest empty house before it
                rebirth = Senet.HOUSE_OF_REBIRTH - board.sum(axis=0)[:Senet.HOUSE_OF_REBIRTH + 1][::-1].tolist().index(0)
                board[player, rebirth] = 1

            # no more pieces on the board
            done = np.sum(board[player]) == 0

            # pass turn if there are 2 or 3 color sides
            pass_turn = num_steps in [2, 3]

        player = player if (not pass_turn) or done else 1 - player
        reward = (1 if player == Senet.CONS_PLAYER else -1) if done else 0

        return board, player, reward, done, pass_turn


class SenetSkyruk(Senet):

    @staticmethod
    def legal_moves(board, player, num_steps):

        clusters = SenetSkyruk.detect_clusters(board, player)

        moves = []

        dancers = np.where(board[player] == 1)[0]
        for dancer_id, dancer in enumerate(dancers):
            landing_house = dancer + num_steps
            # regular piece
            if dancer < Senet.HOUSE_OF_HAPPINESS:
                if landing_house < Senet.HOUSE_OF_HAPPINESS:
                    # no player's dancer in the target house
                    # no protected another dancer's pieces in the target house:
                    # 2 in a row and House of Rebirth
                    # no jumps over blockade: 2 or more in a row
                    # when an opponent's blockade is broken,
                    # no jump oven another blockade is possible:
                    if (board[player, landing_house] == 0
                        and (clusters[landing_house] in [0, 1] and clusters[dancer:landing_house].max(initial=0) < 2
                             or clusters[landing_house] == SenetSkyruk.INNER_DANCER and (clusters[dancer:landing_house] == 2).max(initial=0) == 0)):
                        moves += [SenetSkyruk.encode_move(dancer_id, num_steps)]
                else:
                    # Should stop at House of Happiness anyway if it is empty
                    if (board[:, Senet.HOUSE_OF_HAPPINESS].sum() == 0
                            and clusters[dancer:Senet.HOUSE_OF_HAPPINESS].max(initial=0) != SenetKendall.INNER_DANCER):
                        moves += [SenetSkyruk.encode_move(dancer_id, num_steps)]
            elif dancer == Senet.HOUSE_OF_HAPPINESS:
                # pawn which occupies House of Happiness has to make an extra move
                moves = [SenetSkyruk.encode_move(dancer_id, num_steps)]
                break
            elif dancer == Senet.HOUSE_OF_WATER:
                # pawn makes move if num_steps < 5
                if num_steps < 5:
                    moves += [SenetSkyruk.encode_move(dancer_id, num_steps)]
            elif dancer in [Senet.HOUSE_OF_THREE_TRUTHS, Senet.HOUSE_OF_RE_ATUM]:
                # remove only
                if landing_house == Senet.BOARD_SIZE:
                    moves += [SenetSkyruk.encode_move(dancer_id, num_steps)]
            else:
                # House of Re-Horakthy, can be bourne off with any number of steps
                moves += [SenetSkyruk.encode_move(dancer_id, num_steps)]

        # backward moves when no forward moves are available
        # only for regular houses
        if not moves:
            for dancer_id, dancer in enumerate(dancers):
                if dancer < Senet.HOUSE_OF_HAPPINESS:
                    landing_house = dancer - num_steps
                    if (landing_house >= 0 and board[player, landing_house] == 0
                            and (clusters[landing_house] in [0, 1] and clusters[dancer:landing_house].max(initial=0) < 2
                                 or clusters[landing_house] == SenetSkyruk.INNER_DANCER and (clusters[dancer:landing_house] == 2).max(initial=0) == 0)):
                        moves += [SenetSkyruk.encode_move(dancer_id, -num_steps)]

        # if still no moves are available, add pass turn move
        return moves if moves else [Senet.PASS_TURN]

    @staticmethod
    def apply_move(board, player, move):
        """
        :param board:
        :param player:
        :param move: 0 for pass turn, otherwise move encoded to an integer
        :return:
        """

        if move == Senet.PASS_TURN:
            reward = 0
            done = False
            pass_turn = True
        else:
            dancers = np.where(board[player] == 1)[0]
            dancer_id, num_steps = SenetSkyruk.decode_move(move)

            house = dancers[dancer_id]
            landing_house = house + num_steps

            # correct target house for some special cases
            if house < Senet.HOUSE_OF_HAPPINESS:
                # any pawn should stop at House of Happiness whatever num_steps is
                if landing_house >= Senet.HOUSE_OF_HAPPINESS:
                    landing_house = Senet.HOUSE_OF_HAPPINESS
            elif house == Senet.HOUSE_OF_HAPPINESS:
                # if num_steps = 2, 3, 4 go to the landing house, if it is occupied, go to House of Water
                if landing_house in [Senet.HOUSE_OF_THREE_TRUTHS, Senet.HOUSE_OF_RE_ATUM, Senet.HOUSE_OF_RE_HORAKHTY]:
                    if board[:, landing_house].tolist() != [0, 0]:
                        landing_house = Senet.HOUSE_OF_WATER
                # if num_steps = 1 or target house is occupied and House of Water is occupied as well,
                # go to Rebirth House
                if landing_house == Senet.HOUSE_OF_WATER:
                    if board[:, landing_house].tolist() != [0, 0]:
                        landing_house = SenetSkyruk.rebirth(board)
            elif house == Senet.HOUSE_OF_WATER:
                # if num_steps is 5, standby
                if num_steps == 5:
                    landing_house = house
                # if num_steps is not 4, go to rebirth
                elif num_steps < 4:
                    landing_house = SenetSkyruk.rebirth(board)

            # move player's pawn
            board[player, house] = 0
            if landing_house < Senet.BOARD_SIZE:
                board[player, landing_house] = 1
                # if target house is occupied by opponent's pawn, move it to house of departure
                if board[player - 1, landing_house] == 1:
                    board[player - 1, landing_house] = 0
                    board[player - 1, house] = 1

            # no more pieces on the board
            done = np.sum(board[player] != 0) == 0

            # pass turn if there are 2 or 3 color sides
            # keep turn if target house is one of the last three houses
            pass_turn = (num_steps in [2, 3]) and landing_house != Senet.HOUSE_OF_HAPPINESS

        player = player if (not pass_turn) or done else 1 - player
        reward = (1 if player == Senet.CONS_PLAYER else -1) if done else 0

        return board, player, reward, done, pass_turn

    @staticmethod
    def rebirth(board):
        return Senet.HOUSE_OF_REBIRTH - (board != 0).sum(axis=0)[:Senet.HOUSE_OF_REBIRTH + 1][::-1].tolist().index(0)


class SenetGame:

    @staticmethod
    def gameplay(rules):
        if rules == 'kendall':
            legal_actions = SenetKendall.legal_moves
            apply_action = SenetKendall.apply_move
        elif rules == 'skyruk':
            legal_actions = SenetSkyruk.legal_moves
            apply_action = SenetSkyruk.apply_move
        else:
            raise NotImplementedError(rules)

        return legal_actions, apply_action

    def __init__(self, num_pieces=5, rules='kendall'):

        self.num_pieces = num_pieces
        self.rules = rules

        self.legal_actions, self.apply_action = SenetGame.gameplay(self.rules)

        self.board = np.empty([2, Senet.BOARD_SIZE], dtype=int)
        self.player = None

        self.reset()

    def reset(self):
        self.board = Senet.init_board(self.num_pieces)
        self.player = Senet.SPOOLS_PLAYER
        return self.board, self.player

    def legal_moves(self, sticks):
        return self.legal_actions(self.board, self.player, Senet.steps(sticks))

    def apply_move(self, action):
        self.board, self.player, reward, done, pass_turn = self.apply_action(self.board, self.player, action)
        return self.board, self.player, reward, done, pass_turn

