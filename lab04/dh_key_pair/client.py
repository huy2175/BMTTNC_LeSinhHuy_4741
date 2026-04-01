import socket
import json
import hashlib

class DHClient:
    def __init__(self, host='127.0.0.1', port=12346):
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            raw = sock.recv(8192).decode().strip()
            data = json.loads(raw)
            p = int(data['p'])
            g = int(data['g'])
            A = int(data['A'])

            b = int.from_bytes(hashlib.sha256(b"client-secret").digest(), 'big')
            b = b % (p-2) + 2
            B = pow(g, b, p)

            sock.sendall((json.dumps({'B': str(B)}) + '\n').encode())

            shared = pow(A, b, p)
            key = hashlib.sha256(str(shared).encode()).hexdigest()
            print(f"[CLIENT] Shared key (hex): {key}")

            response = sock.recv(8192).decode()
            print(f"[CLIENT] Server response: {response}")

if __name__ == '__main__':
    DHClient().run()
