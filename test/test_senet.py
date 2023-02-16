import unittest
import numpy as np
from gym_senet.envs.senet import Senet


class TestSenet(unittest.TestCase):

    def test_encode_move(self):
        self.assertEqual(0, Senet.encode_move(Senet.NO_DANCER, 0))
        self.assertEqual(1, Senet.encode_move(0, 1))
        self.assertEqual(24, Senet.encode_move(2, 4))
        self.assertEqual(46, Senet.encode_move(4, -5))
        self.assertEqual(49, Senet.encode_move(4, -2))

    def test_decode_move(self):
        self.assertEqual((Senet.NO_DANCER, 0), Senet.decode_move(0))
        self.assertEqual((1, 1), Senet.decode_move(11))
        self.assertEqual((2, 4), Senet.decode_move(24))
        self.assertEqual((4, -2), Senet.decode_move(49))

    def test_decode_move_for_player(self):
        # given
        board = np.array([
            # -+--+--+--+--+--+--+--+--+--+--+--+--+--+RB+--+--+--+--+--+--+--+--+--+--+HA+WA+3T+RA+HO
            # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # cons
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]   # spools
        ])

        # then
        self.assertEqual((3, 3), Senet.decode_move_for_player(3, board, Senet.CONS_PLAYER))
        self.assertEqual((5, -5), Senet.decode_move_for_player(16, board, Senet.SPOOLS_PLAYER))
        self.assertEqual((23, 5), Senet.decode_move_for_player(45, board, Senet.SPOOLS_PLAYER))
