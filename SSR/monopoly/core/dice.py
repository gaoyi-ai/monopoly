class Dice:

    def __init__(self):
        self.dice1 = None
        self.dice2 = None

    def roll(self, steps) -> int:
        if steps is None:
            import random
            self.dice1 = random.randint(1, 6)
            self.dice2 = random.randint(1, 6)
            steps = self.dice1 + self.dice2
        return steps

