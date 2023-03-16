class Entity:
    def __init__(self, ):
        self.id=None
        self.hp=0
        self.x=0
        self.y=0
        self.speed_x=0
        self.speed_y=0
        
        self.can_move=False

    def move(self, x, y):
        self.x+=x
        self.y+=y