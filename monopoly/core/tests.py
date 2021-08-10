from monopoly.core.game import Game
from monopoly.core.land import ChanceLand
from monopoly.core.move_result import MoveResultType, MoveResult
import unittest

from monopoly.core.player import INIT_PLAYER_MONEY


class GameTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Game(4)
        self.cur_player = self.game.get_current_player()

    def tearDown(self):
        del self.game

    def test_chance_land(self, x=2):
        move_result: MoveResult
        steps, move_result = self.game.roll(x)
        self.assertEqual(x, steps)

        self.game.make_decision(move_result)
        if move_result.get_value() > 0:
            self.assertLess(INIT_PLAYER_MONEY, self.cur_player.get_money())
        else:
            self.assertGreater(INIT_PLAYER_MONEY, self.cur_player.get_money())
        self.assertIsInstance(move_result.get_land().get_content(), ChanceLand)


if __name__ == '__main__':
    unittest.main()
