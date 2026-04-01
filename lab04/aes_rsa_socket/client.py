import socket
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
import json

class Client:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.client_socket = None
        self.server_public_key = None
        self.session_key = None
        
        # Tạo RSA key pair cho client
        self.client_private_key = RSA.generate(2048)
        self.client_public_key = self.client_private_key.publickey()
        
        print("[CLIENT] RSA Key pair generated")

    def receive_key(self):
        """Nhận public key từ server"""
        try:
            # Nhận độ dài key
            key_length_bytes = self.client_socket.recv(4)
            key_length = int.from_bytes(key_length_bytes, 'big')
            
            # Nhận public key
            public_key_pem = b''
            while len(public_key_pem) < key_length:
                packet = self.client_socket.recv(key_length - len(public_key_pem))
                public_key_pem += packet
            
            self.server_public_key = RSA.import_key(public_key_pem)
            print("[CLIENT] Received server public key")
            
        except Exception as e:
            print(f"[CLIENT] Error receiving key: {e}")
            return False
        return True

    def encrypt_message(self, message):
        """Mã hóa message bằng AES và RSA"""
        # Tạo session key ngẫu nhiên cho AES
        self.session_key = get_random_bytes(32)  # 256-bit AES key
        
        # Mã hóa message bằng AES
        cipher_aes = AES.new(self.session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode())
        
        # Mã hóa session key bằng RSA public key của server
        cipher_rsa = PKCS1_OAEP.new(self.server_public_key)
        encrypted_session_key = cipher_rsa.encrypt(self.session_key)
        
        # Đóng gói dữ liệu
        data = {
            'encrypted_key': encrypted_session_key.hex(),
            'ciphertext': ciphertext.hex(),
            'tag': tag.hex()
        }
        
        return json.dumps(data).encode()

    def connect(self):
        """Kết nối đến server"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"[CLIENT] Connected to {self.host}:{self.port}")
            
            # Nhận public key từ server
            if not self.receive_key():
                return False
            
            return True
            
        except Exception as e:
            print(f"[CLIENT] Connection error: {e}")
            return False

    def send_message(self, message):
        """Gửi message đến server"""
        try:
            # Mã hóa message
            encrypted_msg = self.encrypt_message(message)
            
            # Gửi độ dài message
            self.client_socket.sendall(len(encrypted_msg).to_bytes(4, 'big'))
            
            # Gửi message đã mã hóa
            self.client_socket.sendall(encrypted_msg)
            
            # Nhận phản hồi
            response_length_bytes = self.client_socket.recv(4)
            response_length = int.from_bytes(response_length_bytes, 'big')
            
            response = self.client_socket.recv(response_length).decode()
            print(f"[CLIENT] Server response: {response}")
            
        except Exception as e:
            print(f"[CLIENT] Error sending message: {e}")

    def close(self):
        """Đóng kết nối"""
        if self.client_socket:
            self.client_socket.close()
            print("[CLIENT] Connection closed")

def main():
    client = Client()
    
    if not client.connect():
        print("[CLIENT] Failed to connect to server")
        return
    
    print("\n=== Secure Chat Client (AES + RSA) ===")
    print("Type 'quit' to exit\n")
    
    try:
        while True:
            message = input("Enter message: ")
            if message.lower() == 'quit':
                break
            
            if message.strip():
                client.send_message(message)
                
    except KeyboardInterrupt:
        print("\n[CLIENT] Client shutting down...")
    finally:
        client.close()

if __name__ == "__main__":
    main()