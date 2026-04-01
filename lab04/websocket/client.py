import time
from websocket import create_connection

if __name__ == '__main__':
    url = 'ws://127.0.0.1:8888/ws'
    print(f'[WS-CLIENT] Connecting to {url}')
    ws = create_connection(url)
    try:
        while True:
            msg = ws.recv()
            print(f'[WS-CLIENT] Received: {msg}')
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('[WS-CLIENT] Exit')
    except Exception as e:
        print('[WS-CLIENT] Error:', e)
    finally:
        ws.close()
