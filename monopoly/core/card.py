class Card:

    def __init__(self, description, money_deduction, stop_round):
        self.description = description
        self.money_deduction = money_deduction
        self.stop_round = stop_round

    def __repr__(self):
        return f"Card [description:{self.description}, " \
               f"money deduction:{self.money_deduction}, " \
               f"stop round:{self.stop_round}]"

    def __str__(self):
        return self.description
