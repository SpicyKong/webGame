import asyncio
import websockets
import threading
import json

from server import Server

DEBUG=True

SERVER_VERSION="0.0.1"
SERVER_IP="25.11.91.11"
SERVER_PORT=9998


class Network:
    def __init__(self):
        self.socket=None
        self.server=Server()

    async def accept(self, websocket, path):
        try:
            while True:
                data=await websocket.recv()
                data=json.loads(data)
                if DEBUG: print("[CLIENT -> SERVER]", data)
                to_send=network.process(data)
                if to_send!=None:
                    if DEBUG: print("[SERVER -> CLIENT]", to_send)
                    await websocket.send(to_send)
        except Exception as e:
            print("[ERROR_accept]", e)

    def start_server(self):
        self.socket=websockets.serve(self.accept, SERVER_IP, SERVER_PORT)
        asyncio.get_event_loop().run_until_complete(self.socket)
        asyncio.get_event_loop().run_forever()

    def process(self, data):
        to_send=None
        try:
            # 이거를 Server에 넣는게 나을듯
            if "token" not in data:
                if data["qid"]==0: # 첫 접속(클라이언트가 토큰 요청)
                    token=self.server.create_token()
                    if token!=None:
                        to_send='{"qid":0, "token":"'+token+'"}'
                    else:
                        to_send='{"qid":0, "token":"0"}'
            else:
                # 토큰이 올바른 값일때만 Server에서 처리
                if self.server.check_token(data["token"]):
                    to_send=self.server.process(data)
        except Exception as e:
            print("[ERROR_network_process]", e)

        return to_send


if __name__=="__main__":
    network=Network()
    network.start_server()