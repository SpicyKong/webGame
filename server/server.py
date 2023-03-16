from collections import deque

from game.game import Game
import user_token
from user import User

MAX_CCU=30

class Server:
    def __init__(self):
        self.users=[None for _ in range(MAX_CCU)]
        self.rand_q=deque() # 랜덤 매칭 큐

    def find_empty_id(self):
        for i in range(MAX_CCU):
            if self.users[i]==None:
                return i
        return None

    def create_token(self, t):
        user_id=self.find_empty_id()
        if user_id!=None:
            self.users[user_id]=User(user_id)

    def check_token(self, t):
        try:
            t=user_token.decrypt_query(t)
            t=int(t)
            if 0<=t and t<MAX_CCU and self.users[t]!=None:
                return True
        except:
            pass

        return False
    
    def get_user(self, t):
        return int(user_token.decrypt_query(t))

    def process(self, data):
        to_send=None
        try:
            user=user_token.decrypt_query(data["token"])
            # Client가 게임 큐를 돌림
            if data["qid"]==1:
                if data["type"]==0: # 랜덤 큐
                    self.add_q(user)
            else:
                self.game.process(data)
        except Exception as e:
            print("[ERROR_server_process]", e)
        
        return to_send
    
    def add_q(self, user):
        self.rand_q.append(user)
        if len(self.rand_q)>=2:
            p1=self.rand_q.popleft()
            p2=self.rand_q.popleft()
            if p1==p2:
                self.add_q(p1)
            else:
                self.game=Game()
                self.game.start_game()