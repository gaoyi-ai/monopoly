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

    def on_decision_made(self):
        pass

    def on_result_applied(self):
        pass

    def on_pass_start(self):
        pass


class InternalLogHandler(MonopolyHandler):

    def __init__(self, g):
        self.game = g

    def on_error(self, err_msg):
        print('[Error] [Game ID: {0}]'.format(self.game.get_game_id()) + err_msg)

    def on_rolled(self):
        print('[Info] [Game ID: {0}]current player {1} is rolling'.format(
            self.game.get_game_id(), self.game.get_current_player().get_index()))

    def on_decision_made(self):
        print('[Info] [Game ID: {0} ]Decision is made'.format(
            self.game.get_game_id()))

    def on_new_game(self):
        print('[Info] [Game ID: {0}] '.format(self.game.get_game_id()) + \
              "Game Started")

    def on_game_ended(self):
        print('[Info] [Game ID: {0}] '.format(self.game.get_game_id()) + \
              "Game Ended")
        print('[Info] The player {0} has go bankruptcy'.format(
            self.game.get_current_player().get_index()))

    def on_player_changed(self):
        print('[Info] [Game Id: {0}] '.format(self.game.get_game_id()) + \
              "Player changed to : {0}".format(
                  self.game.get_current_player().get_index()))

    def on_result_applied(self):
        pass

    def on_pass_start(self):
        print('[Info] [Game ID: {0}] '.format(self.game.get_game_id()) + \
              "Player {0} just passed the start point".format(
                  self.game.get_current_player().get_index()))
