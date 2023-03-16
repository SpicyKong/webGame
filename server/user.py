class User:
    def __init__(self, id):
        self.id=id
        self.game=None

    def join_game(self, game):
        self.game=game