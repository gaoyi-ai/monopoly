class MonopolyHandler:
    def on_error(self, err_msg):
        pass

    def on_new_game(self):
        pass

    def on_game_ended(self):
        pass

    def on_rolled(self):
        pass

    def on_player_changed(self):
        pass

    def on_decision_made(self, mr):
        pass

    def on_receipt_applied(self, mr):
        pass

    def on_pass_start(self):
        pass


class DebugLogHandler(MonopolyHandler):

    def __init__(self, g):
        self.game = g

    def on_error(self, err_msg):
        print(f'DebugLogHandler [Error] [Game ID: {self.game.game_id}] [Msg: {err_msg}]')

    def on_rolled(self):
        print(f'DebugLogHandler [Info] [Game ID: {self.game.game_id}] [Msg: current player {self.game.cur_player.index} is rolling]')

    def on_decision_made(self, mr):
        print(f'DebugLogHandler [Info] [Game ID: {self.game.game_id}] [Msg: Decision {mr} is made]')

    def on_new_game(self):
        print(f'DebugLogHandler [Info] [Game ID: {self.game.game_id}] [Msg: Game Started]')

    def on_game_ended(self):
        print(f'DebugLogHandler [Info] [Game ID: {self.game.game_id}] [Msg: Game Ended]')
        print(f'DebugLogHandler [Info] [Msg: The player {self.game.cur_player.index} has go bankruptcy]')

    def on_player_changed(self):
        print(f'DebugLogHandler [Info] [Game ID: {self.game.game_id}] [Msg: Player changed to : {self.game.cur_player.index}]')

    def on_receipt_applied(self, mr):
        print(f"DebugLogHandler [Info] [Game ID: {self.game.game_id}] [Msg: Player {self.game.cur_player}'s move result {mr} applied]")

    def on_pass_start(self):
        print(f'DebugLogHandler [Info] [Game ID: {self.game.game_id}] '
              f'[Msg:  Player {self.game.cur_player.index} just passed the start point]')
