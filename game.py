class Game:
    def __init__(self, id):
        self.count1 = 0
        self.count2 = 0
        self.start1 = False
        self.start2 = False
        self.ready = False
        self.id = id


    def connected(self):
        return self.ready

    def winner(self):

        if self.count1 > self.count2:
            winner = 0
        else:
            winner = 1
        return winner

    def resetWent(self):
        self.count1 = 0
        self.count2 = 0

