import socket
import threading
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
import json

class Server:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        
        # Tạo RSA key pair cho server
        self.server_private_key = RSA.generate(2048)
        self.server_public_key = self.server_private_key.publickey()
        
        # Lưu public key ra file
        with open('server_public_key.pem', 'wb') as f:
            f.write(self.server_public_key.export_key())
        
        print("[SERVER] RSA Key pair generated")
        print(f"[SERVER] Public key saved to server_public_key.pem")

    def handle_client(self, client_socket, address):
        """Xử lý kết nối từ client"""
        print(f"[SERVER] New connection from {address}")
        
        try:
            # Gửi public key của server cho client
            public_key_pem = self.server_public_key.export_key()
            client_socket.sendall(len(public_key_pem).to_bytes(4, 'big'))
            client_socket.sendall(public_key_pem)
            
            while True:
                # Nhận độ dài message
                msg_length_bytes = client_socket.recv(4)
                if not msg_length_bytes:
                    break
                
                msg_length = int.from_bytes(msg_length_bytes, 'big')
                
                # Nhận message đã mã hóa
                encrypted_data = b''
                while len(encrypted_data) < msg_length:
                    packet = client_socket.recv(msg_length - len(encrypted_data))
                    if not packet:
                        break
                    encrypted_data += packet
                
                if not encrypted_data:
                    break
                
                # Giải mã và hiển thị
                try:
                    decrypted_msg = encrypted_data.decode('utf-8', errors='ignore')
                    print(f"[SERVER] Received from {address}: {decrypted_msg}")
                    
                    # Gửi phản hồi
                    response = f"Server received: {decrypted_msg}"
                    client_socket.sendall(len(response.encode()).to_bytes(4, 'big'))
                    client_socket.sendall(response.encode())
                    
                except Exception as e:
                    print(f"[SERVER] Error decrypting: {e}")
                    
        except Exception as e:
            print(f"[SERVER] Error handling client {address}: {e}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
            print(f"[SERVER] Connection closed from {address}")

    def start(self):
        """Khởi động server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
        print(f"[SERVER] Server started on {self.host}:{self.port}")
        print(f"[SERVER] Waiting for connections...")
        
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                self.clients.append(client_socket)
                
                # Tạo thread mới để xử lý client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n[SERVER] Server shutting down...")
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = Server()
    server.start()