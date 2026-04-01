import socket
import threading
import json
import hashlib

# DH parameters (demonstration). Thực tế chọn prime 2048-bit nhóm chuẩn.
P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1
G = 2

class DHServer:
    def __init__(self, host='127.0.0.1', port=12346):
        self.host = host
        self.port = port
        self.clients = []

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(5)
        print(f"[SERVER] Listening on {self.host}:{self.port}")
        try:
            while True:
                conn, addr = sock.accept()
                print(f"[SERVER] Connected {addr}")
                thread = threading.Thread(target=self.handle, args=(conn,))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("[SERVER] Shutdown")
        finally:
            sock.close()

    def handle(self, conn):
        try:
            # Step 1: send parameters and server public value
            a = int.from_bytes(hashlib.sha256(b"server-secret").digest(), 'big')
            a = a % (P-2) + 2
            A = pow(G, a, P)
            payload = {'p': str(P), 'g': str(G), 'A': str(A)}
            conn.sendall((json.dumps(payload) + '\n').encode())

            # Step 2: receive B
            data = conn.recv(8192).decode().strip()
            request = json.loads(data)
            B = int(request.get('B'))

            shared = pow(B, a, P)
            key = hashlib.sha256(str(shared).encode()).hexdigest()
            print(f"[SERVER] Shared key (hex): {key}")

            # Step 3: trả lời kiểm tra (plain text để demo):
            conn.sendall(b"DH key exchange success")

        except Exception as e:
            print(f"[SERVER] Error: {e}")
        finally:
            conn.close()

if __name__ == '__main__':
    DHServer().start()
