from monopoly.core.game import Game, GameStateType
from monopoly.core.land import Chance, Infrastructure, Constructable, START_REWARD, BuildingType, Land
from monopoly.core.move_receipt import MoveReceiptType, MoveReceipt
from HwTestReport import HTMLTestReportEN
import unittest

from monopoly.core.player import INIT_PLAYER_MONEY, Player

"""
A test with HTML Report

Note: Run in CLI. If run in Pycharm, set "Run/Debug Configurations", use "Python" not "Python test".
"""


class GameTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.game = Game(2)  # default 2 players
        self.game.game_state = GameStateType.WAIT_FOR_ROLL
        self.player_index = 0
        self.move_receipt = None

    def tearDown(self):
        del self.game

    def test_chance_land(self, x=2):
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(x)
        self.assertEqual(x, steps)

        self.move_receipt = self.game.execute_move_receipt(move_receipt)
        self.assertEqual(self.game.cur_player.index, self.player_index + 1)
        if self.move_receipt.type in [MoveReceiptType.BUY_LAND_OPTION, MoveReceiptType.CONSTRUCTION_OPTION,
                                      MoveReceiptType.PAYMENT]:
            self.assertGreater(INIT_PLAYER_MONEY, self.game.player_index_of(self.player_index).money)
        else:
            self.assertLess(INIT_PLAYER_MONEY, self.game.player_index_of(self.player_index).money)
        self.assertIsInstance(move_receipt.land.content, Chance)

    def test_infrastructure_buy_and_payment(self):
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(5)
        move_receipt.option = True
        infrastructure: Infrastructure = move_receipt.land.content

        self.assertEqual(move_receipt.type, MoveReceiptType.BUY_LAND_OPTION)
        first_player = self.game.cur_player
        self.game.execute_move_receipt(move_receipt)
        # buy
        first_player_money = first_player.money
        self.assertEqual(first_player_money, INIT_PLAYER_MONEY - infrastructure.price)
        self.assertEqual(first_player, infrastructure.owner)

        steps, move_receipt = self.game.roll(5)
        self.assertEqual(move_receipt.type, MoveReceiptType.PAYMENT)
        second_player = self.game.cur_player
        self.game.execute_move_receipt(move_receipt)
        # buy
        self.assertEqual(second_player.money, INIT_PLAYER_MONEY - infrastructure.payment)
        self.assertEqual(first_player.money, first_player_money + move_receipt.value)

    def test_first_player_not_buy_second_buy(self):
        first_player = self.game.cur_player
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(5)
        infrastructure: Infrastructure = move_receipt.land.content
        move_receipt.option = False
        self.game.execute_move_receipt(move_receipt)
        # first not buy
        self.assertEqual(first_player.position, 5)
        self.assertEqual(first_player.money, INIT_PLAYER_MONEY)
        self.assertIsNone(infrastructure.owner)
        # second buy
        second_player = self.game.cur_player
        steps, move_receipt = self.game.roll(5)
        move_receipt.option = True
        self.game.execute_move_receipt(move_receipt)
        self.assertEqual(second_player.position, 5)
        self.assertEqual(second_player.money, INIT_PLAYER_MONEY - infrastructure.price)
        self.assertEqual(infrastructure.owner, second_player)

    def test_two_rounds_buy_payment(self):
        # round1
        first_player = self.game.cur_player
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(3)
        move_receipt.option = False
        self.game.execute_move_receipt(move_receipt)
        self.assertEqual(first_player.money, INIT_PLAYER_MONEY)

        second_player = self.game.cur_player
        steps, move_receipt = self.game.roll(6)
        constructable: Constructable = move_receipt.land.content
        move_receipt.option = True
        self.game.execute_move_receipt(move_receipt)
        second_player_money = second_player.money
        self.assertEqual(second_player_money, INIT_PLAYER_MONEY - constructable.price)
        self.assertEqual(constructable.owner, second_player)

        # round2
        steps, move_receipt = self.game.roll(3)
        constructable: Constructable = move_receipt.land.content
        self.game.execute_move_receipt(move_receipt)
        self.assertEqual(move_receipt.type, MoveReceiptType.PAYMENT)
        self.assertEqual(first_player.money, INIT_PLAYER_MONEY - constructable.toll)
        self.assertEqual(second_player.money, second_player_money + constructable.toll)

    def test_to_jail_stop_one_round(self):
        # round1
        first_player = self.game.cur_player
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(10)
        self.assertEqual(move_receipt.type, MoveReceiptType.STOP_ROUND)
        self.assertEqual(first_player.position, move_receipt.land.pos)
        self.game.execute_move_receipt(move_receipt)

        second_player = self.game.cur_player
        steps, move_receipt = self.game.roll(9)
        move_receipt.option = False
        self.game.execute_move_receipt(move_receipt)

        # round2
        self.assertIs(self.game.cur_player, second_player)
        steps, move_receipt = self.game.roll(5)
        move_receipt.option = False
        self.game.execute_move_receipt(move_receipt)

        # round3
        self.assertIs(self.game.cur_player, first_player)
        steps, move_receipt = self.game.roll(6)
        self.assertEqual(first_player.position, move_receipt.land.pos)

    def test_construct_house(self):
        self.game = Game(1)
        self.game.game_state = GameStateType.WAIT_FOR_ROLL
        player = self.game.cur_player
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(3)
        constructable: Constructable = move_receipt.land.content
        self.assertEqual(move_receipt.type, MoveReceiptType.BUY_LAND_OPTION)
        move_receipt.option = True
        self.game.execute_move_receipt(move_receipt)
        after_buy = player.money
        self.assertEqual(after_buy, INIT_PLAYER_MONEY - constructable.price)

        steps, move_receipt = self.game.roll(40)
        # bypass start
        after_pass_start = player.money
        self.assertEqual(after_pass_start, after_buy + START_REWARD)

        self.assertEqual(move_receipt.type, MoveReceiptType.CONSTRUCTION_OPTION)
        move_receipt.option = True
        self.game.execute_move_receipt(move_receipt)
        after_house = player.money
        self.assertEqual(after_house, after_pass_start - Constructable.HOUSE_CONSTRUCTION_COST)

    def test_another_player_payment_in_construction_land(self):
        # round1
        first_player = self.game.cur_player
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(3)
        constructable: Constructable = move_receipt.land.content
        self.assertEqual(move_receipt.type, MoveReceiptType.BUY_LAND_OPTION)
        move_receipt.option = True
        self.game.execute_move_receipt(move_receipt)
        second_player = self.game.cur_player
        steps, move_receipt = self.game.roll(9)
        move_receipt.option = False
        self.game.execute_move_receipt(move_receipt)

        # round2
        steps, move_receipt = self.game.roll(40)
        self.assertEqual(move_receipt.type, MoveReceiptType.CONSTRUCTION_OPTION)
        move_receipt.option = True
        self.game.execute_move_receipt(move_receipt)
        first_player_after_house = first_player.money
        self.assertEqual(first_player_after_house,
                         INIT_PLAYER_MONEY + START_REWARD - constructable.price - Constructable.HOUSE_CONSTRUCTION_COST)

        steps, move_receipt = self.game.roll(34)
        self.assertEqual(move_receipt.type, MoveReceiptType.PAYMENT)
        self.game.execute_move_receipt(move_receipt)
        self.assertEqual(second_player.money, INIT_PLAYER_MONEY + START_REWARD - constructable.toll)

    def test_parking(self):
        self.game = Game(1)
        self.game.game_state = GameStateType.WAIT_FOR_ROLL
        # round1
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(20)
        self.assertEqual(move_receipt.type, MoveReceiptType.NOTHING)
        self.game.execute_move_receipt(move_receipt)
        player = self.game.cur_player
        round_one_money = player.money
        # round2
        steps, move_receipt = self.game.roll(21)
        move_receipt.option = False
        self.game.execute_move_receipt(move_receipt)
        self.assertEqual(player.money, round_one_money + START_REWARD)

    def test_bypass_on_start(self):
        self.game = Game(1)
        self.game.game_state = GameStateType.WAIT_FOR_ROLL
        # round1
        player = self.game.cur_player
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(40)
        self.assertEqual(player.position, move_receipt.land.pos)
        self.game.execute_move_receipt(move_receipt)
        self.assertEqual(player.money, INIT_PLAYER_MONEY + START_REWARD)

    def test_hotel(self):
        self.game = Game(1)
        self.game.game_state = GameStateType.WAIT_FOR_ROLL
        # round1
        player = self.game.cur_player
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(8)
        land: Land = move_receipt.land
        constructable: Constructable = land.content
        self.assertEqual(move_receipt.type, MoveReceiptType.BUY_LAND_OPTION)
        move_receipt.option = True
        self.game.execute_move_receipt(move_receipt)
        after_buy = player.money

        self.assertEqual(after_buy, INIT_PLAYER_MONEY - constructable.price)
        self.assertIs(constructable.owner, player)
        self.assertEqual(constructable.building_num, 0)
        self.assertTrue(constructable.is_constructable())
        self.assertEqual(constructable.property_type, BuildingType.NOTHING)

        for i in range(1, 4):  # round 2 3 4
            steps, move_receipt = self.game.roll(40)
            self.assertEqual(move_receipt.type, MoveReceiptType.CONSTRUCTION_OPTION)
            move_receipt.option = True
            self.game.execute_move_receipt(move_receipt)
            after_construct = player.money
            self.assertEqual(after_construct,
                             after_buy + START_REWARD * i - Constructable.HOUSE_CONSTRUCTION_COST * i)
            self.assertEqual(constructable.building_num, i)
            self.assertTrue(constructable.is_constructable())
            self.assertEqual(constructable.property_type, BuildingType.HOUSE)
            self.assertEqual(land.evaluate(), constructable.price + Constructable.HOUSE_CONSTRUCTION_COST * i)

        self.game.players.append(Player(1))
        steps, move_receipt = self.game.roll(40)
        self.assertEqual(move_receipt.type, MoveReceiptType.CONSTRUCTION_OPTION)
        move_receipt.option = True
        self.game.execute_move_receipt(move_receipt)
        after_construct = player.money
        self.assertEqual(after_construct,
                         after_buy + START_REWARD * 4 -
                         Constructable.HOUSE_CONSTRUCTION_COST * 3 - Constructable.HOTEL_CONSTRUCTION_COST)
        self.assertEqual(constructable.building_num, 1)
        self.assertFalse(constructable.is_constructable())
        self.assertEqual(constructable.property_type, BuildingType.HOTEL)
        self.assertEqual(land.evaluate(), constructable.price + Constructable.HOUSE_CONSTRUCTION_COST * 3 +
                         Constructable.HOTEL_CONSTRUCTION_COST)

        steps, move_receipt = self.game.roll(8)
        self.assertEqual(move_receipt.type, MoveReceiptType.PAYMENT)
        second_player = self.game.cur_player
        self.game.execute_move_receipt(move_receipt)
        self.assertEqual(second_player.money, INIT_PLAYER_MONEY - constructable.toll)
        self.assertEqual(player.money, after_construct + constructable.toll)

    def test_no_enough_money_to_buy(self):
        self.game = Game(1)
        self.game.game_state = GameStateType.WAIT_FOR_ROLL
        player = self.game.cur_player
        player.money = 1
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(12)
        infrastructure: Infrastructure = move_receipt.land.content
        move_receipt.option = True
        self.assertLess(player.money, infrastructure.price)
        self.assertEqual(self.game.execute_move_receipt(move_receipt).type, MoveReceiptType.NOTHING)

    def test_no_enough_money_to_construct_building(self):
        self.game = Game(1)
        self.game.game_state = GameStateType.WAIT_FOR_ROLL
        # round1
        player = self.game.cur_player
        player.money = 70
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(3)
        constructable: Constructable = move_receipt.land.content
        move_receipt.option = True
        self.game.execute_move_receipt(move_receipt)
        self.assertIs(constructable.owner, player)

        # round2
        steps, move_receipt = self.game.roll(40)
        self.assertEqual(move_receipt.type, MoveReceiptType.CONSTRUCTION_OPTION)
        player.money = 70
        move_receipt.option = True
        self.game.execute_move_receipt(move_receipt)
        self.assertEqual(self.game.execute_move_receipt(move_receipt).type, MoveReceiptType.NOTHING)

    def test_arrive_second_time_to_infrastructure(self):
        self.game = Game(1)
        self.game.game_state = GameStateType.WAIT_FOR_ROLL
        # round1
        player = self.game.cur_player
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(5)
        infrastructure: Infrastructure = move_receipt.land.content
        move_receipt.option = True
        self.game.execute_move_receipt(move_receipt)
        self.assertIs(infrastructure.owner, player)
        # round2
        steps, move_receipt = self.game.roll(40)
        self.assertEqual(move_receipt.type, MoveReceiptType.NOTHING)
        self.assertEqual(player.money, INIT_PLAYER_MONEY + START_REWARD - infrastructure.price)

    def test_game_end(self):
        # round1
        first_player = self.game.cur_player
        first_player.money = 70
        move_receipt: MoveReceipt
        steps, move_receipt = self.game.roll(3)
        constructable: Constructable = move_receipt.land.content
        move_receipt.option = True
        self.game.execute_move_receipt(move_receipt)
        self.assertIs(constructable.owner, first_player)

        second_player = self.game.cur_player
        second_player.money = 1

        steps, move_receipt = self.game.roll(3)
        self.assertEqual(move_receipt.type, MoveReceiptType.PAYMENT)
        self.game.execute_move_receipt(move_receipt)
        self.assertEqual(self.game.game_state, GameStateType.GAME_ENDED)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(GameTestCase('test_chance_land'))
    suite.addTest(GameTestCase('test_infrastructure_buy_and_payment'))
    suite.addTest(GameTestCase('test_first_player_not_buy_second_buy'))
    suite.addTest(GameTestCase('test_two_rounds_buy_payment'))
    suite.addTest(GameTestCase('test_to_jail_stop_one_round'))
    suite.addTest(GameTestCase('test_construct_house'))
    suite.addTest(GameTestCase('test_another_player_payment_in_construction_land'))
    suite.addTest(GameTestCase('test_parking'))
    suite.addTest(GameTestCase('test_bypass_on_start'))
    suite.addTest(GameTestCase('test_hotel'))
    suite.addTest(GameTestCase('test_no_enough_money_to_buy'))
    suite.addTest(GameTestCase('test_no_enough_money_to_construct_building'))
    suite.addTest(GameTestCase('test_arrive_second_time_to_infrastructure'))
    suite.addTest(GameTestCase('test_game_end'))
    with open('./HwTestReportEN.html', 'wb') as report:
        runner = HTMLTestReportEN(stream=report,
                                  verbosity=2,
                                  title='Default test',
                                  description='description_placeholder',
                                  tester='Yi, Haoyu')
        runner.run(suite)
