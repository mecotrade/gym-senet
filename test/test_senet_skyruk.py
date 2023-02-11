import unittest
import numpy as np
from gym_senet.envs.senet import SenetSkyruk


class TestSenetSkyruk(unittest.TestCase):

    def test_legal_moves_blockade(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([(3, -1)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 1))
        self.assertEqual([(3, -2)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 2))
        self.assertEqual([(3, -3)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 3))
        self.assertEqual([(SenetSkyruk.BOARD_SIZE, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 4))
        self.assertEqual([(SenetSkyruk.BOARD_SIZE, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 5))

    def test_legal_moves_break_blockade(self):
            # given
            board = np.array([
                # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
                # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # cons
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # spools
            ])

            # then
            self.assertEqual([(3, -1)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 1))
            self.assertEqual([(3, 2)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 2))
            self.assertEqual([(3, 3)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 3))
            self.assertEqual([(SenetSkyruk.BOARD_SIZE, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 4))
            self.assertEqual([(SenetSkyruk.BOARD_SIZE, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 5))

    def test_legal_moves_no_break_blockade(self):
            # given
            board = np.array([
                # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
                # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # cons
                [0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # spools
            ])

            # then
            self.assertEqual([(3, -1)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 1))
            self.assertEqual([(3, -2)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 2))
            self.assertEqual([(3, -3)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 3))
            self.assertEqual([(SenetSkyruk.BOARD_SIZE, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 4))
            self.assertEqual([(SenetSkyruk.BOARD_SIZE, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 5))

    def test_legal_moves_jump_over_single_dancer(self):
            # given
            board = np.array([
                # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
                # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # cons
                [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # spools
            ])

            # then
            self.assertEqual([(3, 1)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 1))
            self.assertEqual([(3, 2)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 2))
            self.assertEqual([(3, -3)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 3))
            self.assertEqual([(3, 4)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 4))
            self.assertEqual([(3, 5)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 5))


    def test_legal_moves_house_of_happiness_empty(self):
            # given
            board = np.array([
                # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
                # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # cons
                [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]  # spools
            ])

            # then
            self.assertEqual([(22, 1)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 1))
            self.assertEqual([(22, 2)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 2))
            self.assertEqual([(22, 3)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 3))
            self.assertEqual([(22, 4)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 4))
            self.assertEqual([(22, 5)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 5))

    def test_legal_moves_house_of_happiness_not_empty(self):
            # given
            board = np.array([
                # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
                # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # cons
                [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]  # spools
            ])

            # then
            self.assertEqual([(22, 1)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 1))
            self.assertEqual([(22, -2)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 2))
            self.assertEqual([(22, -3)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 3))
            self.assertEqual([(22, -4)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 4))
            self.assertEqual([(22, -5)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 5))

    def test_apply_moves_stop_at_house_of_happiness(self):
        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]  # spools
        ])

        # then
        self.assertEqual([(22, 5)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 5))


        # when
        new_board, player, player_wins, pass_turn = SenetSkyruk.apply_move(board, SenetSkyruk.CONS_PLAYER, (22, 5))
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
                         new_board[SenetSkyruk.CONS_PLAYER].tolist())
        self.assertEqual(SenetSkyruk.CONS_PLAYER, player)
        self.assertFalse(player_wins)
        self.assertFalse(pass_turn)

