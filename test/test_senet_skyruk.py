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
        self.assertEqual([SenetSkyruk.encode_move(0, -1)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 1))
        self.assertEqual([SenetSkyruk.encode_move(0, -2)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 2))
        self.assertEqual([SenetSkyruk.encode_move(0, -3)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 3))
        self.assertEqual([SenetSkyruk.encode_move(SenetSkyruk.NO_DANCER, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 4))
        self.assertEqual([SenetSkyruk.encode_move(SenetSkyruk.NO_DANCER, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 5))

    def test_legal_moves_break_blockade(self):
        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetSkyruk.encode_move(0, -1)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 1))
        self.assertEqual([SenetSkyruk.encode_move(0, 2)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 2))
        self.assertEqual([SenetSkyruk.encode_move(0, 3)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 3))
        self.assertEqual([SenetSkyruk.encode_move(SenetSkyruk.NO_DANCER, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 4))
        self.assertEqual([SenetSkyruk.encode_move(SenetSkyruk.NO_DANCER, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 5))

    def test_legal_moves_no_break_blockade(self):
        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # spools
        ])

        # then
        self.assertEqual([SenetSkyruk.encode_move(0, -1)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 1))
        self.assertEqual([SenetSkyruk.encode_move(0, -2)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 2))
        self.assertEqual([SenetSkyruk.encode_move(0, -3)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 3))
        self.assertEqual([SenetSkyruk.encode_move(SenetSkyruk.NO_DANCER, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 4))
        self.assertEqual([SenetSkyruk.encode_move(SenetSkyruk.NO_DANCER, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 5))

    def test_legal_moves_jump_over_single_dancer(self):
        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # spools
        ])

        # then
        self.assertEqual([SenetSkyruk.encode_move(0, 1)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 1))
        self.assertEqual([SenetSkyruk.encode_move(0, 2)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 2))
        self.assertEqual([SenetSkyruk.encode_move(0, -3)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 3))
        self.assertEqual([SenetSkyruk.encode_move(0, 4)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 4))
        self.assertEqual([SenetSkyruk.encode_move(0, 5)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 5))

    def test_legal_moves_house_of_happiness_empty(self):
        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]  # spools
        ])

        # then
        self.assertEqual([SenetSkyruk.encode_move(0, 1)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 1))
        self.assertEqual([SenetSkyruk.encode_move(0, 2)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 2))
        self.assertEqual([SenetSkyruk.encode_move(0, 3)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 3))
        self.assertEqual([SenetSkyruk.encode_move(0, 4)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 4))
        self.assertEqual([SenetSkyruk.encode_move(0, 5)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 5))

    def test_legal_moves_house_of_happiness_not_empty(self):
        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]  # spools
        ])

        # then
        self.assertEqual([SenetSkyruk.encode_move(0, 1)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 1))
        self.assertEqual([SenetSkyruk.encode_move(0, -2)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 2))
        self.assertEqual([SenetSkyruk.encode_move(0, -3)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 3))
        self.assertEqual([SenetSkyruk.encode_move(0, -4)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 4))
        self.assertEqual([SenetSkyruk.encode_move(0, -5)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 5))

    def test_legal_moves_from_house_of_happiness(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetSkyruk.encode_move(4, 1)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 1))
        self.assertEqual([SenetSkyruk.encode_move(4, 2)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 2))
        self.assertEqual([SenetSkyruk.encode_move(4, 3)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 3))
        self.assertEqual([SenetSkyruk.encode_move(4, 4)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 4))
        self.assertEqual([SenetSkyruk.encode_move(4, 5)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 5))

    def test_legal_moves_from_house_of_three_truths(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]   # spools
        ])

        # then
        self.assertEqual([SenetSkyruk.encode_move(SenetSkyruk.NO_DANCER, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 1))
        self.assertEqual([SenetSkyruk.encode_move(1, 2)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 2))
        self.assertEqual([SenetSkyruk.encode_move(0, 3)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 3))
        self.assertEqual([SenetSkyruk.encode_move(SenetSkyruk.NO_DANCER, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 4))
        self.assertEqual([SenetSkyruk.encode_move(SenetSkyruk.NO_DANCER, 0)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 5))

    def test_legal_moves_from_house_of_re_horakhty(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]   # spools
        ])

        # then
        self.assertEqual([SenetSkyruk.encode_move(0, 1)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 1))
        self.assertEqual([SenetSkyruk.encode_move(0, 2)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 2))
        self.assertEqual([SenetSkyruk.encode_move(0, 3)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 3))
        self.assertEqual([SenetSkyruk.encode_move(0, 4)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 4))
        self.assertEqual([SenetSkyruk.encode_move(0, 5)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 5))

    def test_apply_moves_stop_at_house_of_happiness(self):
        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]   # spools
        ])

        # when
        self.assertEqual([SenetSkyruk.encode_move(0, 3)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 3))

        # then
        new_board, player, reward, done, pass_turn = SenetSkyruk.apply_move(board.copy(), SenetSkyruk.CONS_PLAYER, SenetSkyruk.encode_move(0, 3))
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                         new_board[SenetSkyruk.CONS_PLAYER].tolist())
        self.assertEqual(SenetSkyruk.CONS_PLAYER, player)
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertFalse(pass_turn)

        # when
        self.assertEqual([SenetSkyruk.encode_move(0, 5)], SenetSkyruk.legal_moves(board, SenetSkyruk.CONS_PLAYER, 5))

        # then
        new_board, player, reward, done, pass_turn = SenetSkyruk.apply_move(board.copy(), SenetSkyruk.CONS_PLAYER, SenetSkyruk.encode_move(0, 5))
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                         new_board[SenetSkyruk.CONS_PLAYER].tolist())
        self.assertEqual(SenetSkyruk.CONS_PLAYER, player)
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertFalse(pass_turn)

    def test_apply_moves_from_house_of_happiness(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0]   # spools
        ])

        # when
        self.assertEqual([SenetSkyruk.encode_move(4, 1)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 1))

        # then
        new_board, player, reward, done, pass_turn = SenetSkyruk.apply_move(board.copy(), SenetSkyruk.SPOOLS_PLAYER, SenetSkyruk.encode_move(4, 1))
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                         new_board[SenetSkyruk.SPOOLS_PLAYER].tolist())
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertFalse(pass_turn)

        # when
        self.assertEqual([SenetSkyruk.encode_move(4, 2)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 2))

        # then
        new_board, player, reward, done, pass_turn = SenetSkyruk.apply_move(board.copy(), SenetSkyruk.SPOOLS_PLAYER, SenetSkyruk.encode_move(4, 2))
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                         new_board[SenetSkyruk.SPOOLS_PLAYER].tolist())
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertTrue(pass_turn)

        # when
        self.assertEqual([SenetSkyruk.encode_move(4, 3)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 3))

        # then
        new_board, player, reward, done, pass_turn = SenetSkyruk.apply_move(board.copy(), SenetSkyruk.SPOOLS_PLAYER, SenetSkyruk.encode_move(4, 3))
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                         new_board[SenetSkyruk.SPOOLS_PLAYER].tolist())
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertTrue(pass_turn)

        # when
        self.assertEqual([SenetSkyruk.encode_move(4, 4)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 4))

        # then
        new_board, player, reward, done, pass_turn = SenetSkyruk.apply_move(board.copy(), SenetSkyruk.SPOOLS_PLAYER, SenetSkyruk.encode_move(4, 4))
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                         new_board[SenetSkyruk.SPOOLS_PLAYER].tolist())
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertFalse(pass_turn)

        # when
        self.assertEqual([SenetSkyruk.encode_move(4, 5)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 5))

        # then
        new_board, player, reward, done, pass_turn = SenetSkyruk.apply_move(board.copy(), SenetSkyruk.SPOOLS_PLAYER, SenetSkyruk.encode_move(4, 5))
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                         new_board[SenetSkyruk.SPOOLS_PLAYER].tolist())
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertFalse(pass_turn)

    def test_apply_moves_from_house_of_happiness_house_of_water_occupied(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0]   # spools
        ])

        # when
        self.assertEqual([SenetSkyruk.encode_move(4, 1)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 1))

        # then
        new_board, player, reward, done, pass_turn = SenetSkyruk.apply_move(board.copy(), SenetSkyruk.SPOOLS_PLAYER, SenetSkyruk.encode_move(4, 1))
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                         new_board[SenetSkyruk.SPOOLS_PLAYER].tolist())
        self.assertEqual(SenetSkyruk.SPOOLS_PLAYER, player)
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertFalse(pass_turn)

        # when
        self.assertEqual([SenetSkyruk.encode_move(4, 2)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 2))

        # then
        new_board, player, reward, done, pass_turn = SenetSkyruk.apply_move(board.copy(), SenetSkyruk.SPOOLS_PLAYER, SenetSkyruk.encode_move(4, 2))
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                         new_board[SenetSkyruk.SPOOLS_PLAYER].tolist())
        self.assertEqual(SenetSkyruk.CONS_PLAYER, player)
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertTrue(pass_turn)

        # when
        self.assertEqual([SenetSkyruk.encode_move(4, 3)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 3))

        # then
        new_board, player, reward, done, pass_turn = SenetSkyruk.apply_move(board.copy(), SenetSkyruk.SPOOLS_PLAYER, SenetSkyruk.encode_move(4, 3))
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                         new_board[SenetSkyruk.SPOOLS_PLAYER].tolist())
        self.assertEqual(SenetSkyruk.CONS_PLAYER, player)
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertTrue(pass_turn)

        # when
        self.assertEqual([SenetSkyruk.encode_move(4, 4)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 4))

        # then
        new_board, player, reward, done, pass_turn = SenetSkyruk.apply_move(board.copy(), SenetSkyruk.SPOOLS_PLAYER, SenetSkyruk.encode_move(4, 4))
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                         new_board[SenetSkyruk.SPOOLS_PLAYER].tolist())
        self.assertEqual(SenetSkyruk.SPOOLS_PLAYER, player)
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertFalse(pass_turn)

        # when
        self.assertEqual([SenetSkyruk.encode_move(4, 5)], SenetSkyruk.legal_moves(board, SenetSkyruk.SPOOLS_PLAYER, 5))

        # then
        new_board, player, reward, done, pass_turn = SenetSkyruk.apply_move(board.copy(), SenetSkyruk.SPOOLS_PLAYER, SenetSkyruk.encode_move(4, 5))
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                         new_board[SenetSkyruk.SPOOLS_PLAYER].tolist())
        self.assertEqual(SenetSkyruk.SPOOLS_PLAYER, player)
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertFalse(pass_turn)
