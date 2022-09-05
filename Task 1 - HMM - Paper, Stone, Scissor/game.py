class Game:
    STONE = 0
    SCISSORS = 1
    PAPER = 2

    WIN = 1
    DRAW = 0
    LOSS = -1 

    rules = [
        [DRAW, WIN, LOSS], # stone
        [LOSS, DRAW, WIN], # scissors
        [WIN, LOSS, DRAW]  # paper
    ]

    prev_move = None

    def move(self, move):
        if self.prev_move == None:
            self.prev_move = move
            return -2
        else:
            result = self.rules[self.prev_move][move]
            self.prev_move = None
            return result