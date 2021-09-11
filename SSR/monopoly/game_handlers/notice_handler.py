from monopoly.core.util import MonopolyHandler
import logging

logger = logging.getLogger(__name__)


class NoticeHandler(MonopolyHandler):
    def __init__(self, game, hostname):
        self.game = game
        self.hostname = hostname
        self.game_end = False
        self.is_bypass_start = False

    def on_pass_start(self):
        self.is_bypass_start = True
        logger.info('bypass start point')

    def on_error(self, err_msg):
        logger.info(f"Sorry. error: {err_msg}")

    def on_rolled(self):
        logger.info(f'[Info] the player {self.game.cur_player.index} is rolling')

    def on_decision_made(self, mr):
        logger.info('[Info] Decision is made, the decision is')

    def on_new_game(self):
        logger.info('it is the start of the game')

    def on_game_ended(self):
        self.game_end = True
        logger.info('this is the end of the game')

    def on_player_changed(self):
        pass

    def on_receipt_applied(self, mr):
        pass
