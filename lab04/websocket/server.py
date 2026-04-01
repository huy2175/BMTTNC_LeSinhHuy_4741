import tornado.ioloop
import tornado.web
import tornado.websocket
import json

fruits = ['Apple','Banana','Cherry','Date','Mango','Orange','Pineapple','Grape','Kiwi']
clients = set()
index = 0

class FruitSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        clients.add(self)
        self.write_message('Connected to Tornado WebSocket server')
        print('[WS] New client connected', self.request.remote_ip)

    def on_message(self, message):
        print('[WS] Received:', message)

    def on_close(self):
        clients.discard(self)
        print('[WS] Client disconnected', self.request.remote_ip)

    def check_origin(self, origin):
        return True


def broadcast_fruit():
    global index
    if not clients:
        return
    fruit = fruits[index % len(fruits)]
    index += 1
    payload = json.dumps({'fruit': fruit})
    for c in list(clients):
        try:
            c.write_message(payload)
        except Exception as e:
            print('[WS] Send error', e)
            clients.discard(c)
    print('[WS] Broadcast:', payload)


def make_app():
    return tornado.web.Application([
        (r'/ws', FruitSocket),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    print('[WS] Tornado server running at ws://127.0.0.1:8888/ws')
    tornado.ioloop.PeriodicCallback(broadcast_fruit, 3000).start()
    tornado.ioloop.IOLoop.current().start()
