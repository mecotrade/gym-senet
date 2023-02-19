import unittest
import numpy as np
from gym_senet.envs.senet import SenetKendall


class TestSenetKendall(unittest.TestCase):

    def test_legal_moves_protected(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(0, -1)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 1))
        self.assertEqual([SenetKendall.encode_move(0, -2)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 2))
        self.assertEqual([SenetKendall.encode_move(0, 3)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 3))
        self.assertEqual([SenetKendall.encode_move(0, 4)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 4))
        self.assertEqual([SenetKendall.encode_move(0, 5)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 5))

    def test_legal_moves_blockade(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(0, -1)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 1))
        self.assertEqual([SenetKendall.encode_move(0, -2)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 2))
        self.assertEqual([SenetKendall.encode_move(0, -3)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 3))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 4))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 5))

    def test_legal_moves_protected_with_house_of_happiness(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(0, 1)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 1))
        self.assertEqual([SenetKendall.encode_move(0, -2)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 2))
        self.assertEqual([SenetKendall.encode_move(0, -3)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 3))
        self.assertEqual([SenetKendall.encode_move(0, -4)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 4))
        self.assertEqual([SenetKendall.encode_move(0, -5)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 5))

    def test_legal_moves_house_of_happiness(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(0, 1)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 1))
        self.assertEqual([SenetKendall.encode_move(0, -2)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 2))
        self.assertEqual([SenetKendall.encode_move(0, -3)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 3))
        self.assertEqual([SenetKendall.encode_move(0, 4)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 4))
        self.assertEqual([SenetKendall.encode_move(0, -5)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 5))

    def test_legal_moves_house_of_happiness_blockade(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(0, -1)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 1))
        self.assertEqual([SenetKendall.encode_move(0, -2)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 2))
        self.assertEqual([SenetKendall.encode_move(0, -3)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 3))
        self.assertEqual([SenetKendall.encode_move(0, -4)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 4))
        self.assertEqual([SenetKendall.encode_move(0, -5)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 5))

    def test_legal_moves_between_blockades(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(0, -1)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 1))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 2))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 3))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 4))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 5))

    def test_legal_moves_house_of_rebirth_protected(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(0, 1)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 1))
        self.assertEqual([SenetKendall.encode_move(0, -2)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 2))
        self.assertEqual([SenetKendall.encode_move(0, 3)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 3))
        self.assertEqual([SenetKendall.encode_move(0, 4)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 4))
        self.assertEqual([SenetKendall.encode_move(0, 5)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 5))

    def test_legal_moves_from_house_of_happiness(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(0, 1)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 1))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 2))
        self.assertEqual([SenetKendall.encode_move(0, 3)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 3))
        self.assertEqual([SenetKendall.encode_move(0, 4)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 4))
        self.assertEqual([SenetKendall.encode_move(0, 5)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 5))

    def test_legal_moves_from_house_of_three_truths(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 1))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 2))
        self.assertEqual([SenetKendall.encode_move(0, 3)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 3))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 4))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 5))

    def test_legal_moves_from_house_of_ra_atum(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 1))
        self.assertEqual([SenetKendall.encode_move(0, 2)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 2))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 3))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 4))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 5))

    def test_legal_moves_backward(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(0, -1)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 1))
        self.assertEqual([SenetKendall.encode_move(0, -2)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 2))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 3))
        self.assertEqual([SenetKendall.encode_move(0, -4)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 4))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 5))

    def test_legal_moves_backward_house_of_happiness(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(0, 1)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 1))
        self.assertEqual([SenetKendall.encode_move(0, -2)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 2))
        self.assertEqual([SenetKendall.encode_move(0, -3)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 3))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 4))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 5))

    def test_legal_moves_backward_takes(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 1))
        self.assertEqual([SenetKendall.encode_move(SenetKendall.NO_DANCER, 0)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 2))
        self.assertEqual([SenetKendall.encode_move(0, -3)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 3))
        self.assertEqual([SenetKendall.encode_move(0, -4)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 4))
        self.assertEqual([SenetKendall.encode_move(0, -5)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 5))

    def test_apply_move_to_house_of_water(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(0, 1)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 1))

        # when
        new_board, player, reward, done, pass_turn = SenetKendall.apply_move(board, SenetKendall.SPOOLS_PLAYER, SenetKendall.encode_move(0, 1))

        # then
        # check side effects on the board
        self.assertTrue(new_board.tolist() == board.tolist())
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         new_board[SenetKendall.SPOOLS_PLAYER].tolist())
        self.assertEqual(SenetKendall.SPOOLS_PLAYER, player)
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertFalse(pass_turn)

    def test_apply_move_to_house_of_water_house_of_rebirth_occupied(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(0, 1)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 1))

        # when
        new_board, player, reward, done, pass_turn = SenetKendall.apply_move(board, SenetKendall.SPOOLS_PLAYER, SenetKendall.encode_move(0, 1))

        # then
        # check side effects on the board
        self.assertTrue(new_board.tolist() == board.tolist())
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         new_board[SenetKendall.SPOOLS_PLAYER].tolist())
        self.assertEqual(SenetKendall.SPOOLS_PLAYER, player)
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertFalse(pass_turn)

    def test_apply_move_house_of_water_happiness_wins(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(0, 5)], SenetKendall.legal_moves(board, SenetKendall.SPOOLS_PLAYER, 5))

        # when
        new_board, player, reward, done, pass_turn = SenetKendall.apply_move(board, SenetKendall.SPOOLS_PLAYER, SenetKendall.encode_move(0, 5))

        # then
        # check side effects on the board
        self.assertTrue(new_board.tolist() == board.tolist())
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|2
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         new_board[SenetKendall.SPOOLS_PLAYER].tolist())
        self.assertEqual(SenetKendall.SPOOLS_PLAYER, player)
        self.assertTrue(done)
        self.assertEqual(-1, reward)
        self.assertFalse(pass_turn)

    def test_apply_move_last_dancer(self):

        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # cons
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual([SenetKendall.encode_move(-1, 0)], SenetKendall.legal_moves(board, SenetKendall.CONS_PLAYER, 1))

        # when
        new_board, player, reward, done, pass_turn = SenetKendall.apply_move(board, SenetKendall.CONS_PLAYER, SenetKendall.encode_move(-1, 0))

        # then
        #                 -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
        #                 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|2
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                         new_board[SenetKendall.CONS_PLAYER].tolist())
        self.assertEqual(SenetKendall.SPOOLS_PLAYER, player)
        self.assertEqual(0, reward)
        self.assertFalse(done)
        self.assertTrue(pass_turn)
