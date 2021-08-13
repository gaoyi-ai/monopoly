from monopoly.core.game import Game
from monopoly.core.land import Chance
from monopoly.core.move_receipt import MoveReceiptType, MoveReceipt
import unittest

from monopoly.core.player import INIT_PLAYER_MONEY


class GameTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.game = Game(4)
        self.player_index = 0
        self.move_receipt = None

    def tearDown(self):
        del self.game

    def test_chance_land(self, x=2):
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(x)
        self.assertEqual(x, steps)

        self.move_receipt = self.game.determinate_move_receipt(move_receipt)
        self.assertEqual(self.game.cur_player.index, self.player_index + 1)
        if self.move_receipt.type in [MoveReceiptType.BUY_LAND_OPTION, MoveReceiptType.CONSTRUCTION_OPTION,
                                      MoveReceiptType.PAYMENT]:
            self.assertGreater(INIT_PLAYER_MONEY, self.game.player_index_of(self.player_index).money)
        else:
            self.assertLess(INIT_PLAYER_MONEY, self.game.player_index_of(self.player_index).money)
        self.assertIsInstance(move_receipt.land.content, Chance)


if __name__ == '__main__':
    unittest.main()
