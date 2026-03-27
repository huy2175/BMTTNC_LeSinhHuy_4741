import ecdsa
import hashlib
import os
import binascii

# Đảm bảo folder keys tồn tại
key_dir = os.path.join(os.path.dirname(__file__), 'keys')
if not os.path.exists(key_dir):
    os.makedirs(key_dir)

class ECCCipher:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        """Tạo cặp khóa ECC"""
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        self.public_key = self.private_key.get_verifying_key()
        
        # Lưu private key
        with open(os.path.join(key_dir, 'private_key.pem'), 'wb') as f:
            f.write(self.private_key.to_pem())
        
        # Lưu public key
        with open(os.path.join(key_dir, 'public_key.pem'), 'wb') as f:
            f.write(self.public_key.to_pem())
        
        return True

    def load_keys(self):
        """Nạp khóa từ file"""
        try:
            with open(os.path.join(key_dir, 'private_key.pem'), 'rb') as f:
                self.private_key = ecdsa.SigningKey.from_pem(f.read())
            
            with open(os.path.join(key_dir, 'public_key.pem'), 'rb') as f:
                self.public_key = ecdsa.VerifyingKey.from_pem(f.read())
            
            return self.private_key, self.public_key
        except FileNotFoundError:
            return None, None

    def sign(self, message):
        """Ký số thông điệp"""
        if not self.private_key:
            return None
        
        # Hash message với SHA-256
        message_hash = hashlib.sha256(message.encode('utf-8')).digest()
        
        # Ký số
        signature = self.private_key.sign(message_hash)
        
        return binascii.hexlify(signature).decode('utf-8')

    def verify(self, message, signature_hex):
        """Xác thực chữ ký"""
        if not self.public_key:
            return False
        
        try:
            # Hash message
            message_hash = hashlib.sha256(message.encode('utf-8')).digest()
            
            # Convert signature từ hex sang bytes
            signature = binascii.unhexlify(signature_hex.encode('utf-8'))
            
            # Verify
            self.public_key.verify(signature, message_hash)
            return True
        except ecdsa.BadSignatureError:
            return False
        except Exception as e:
            print(f"Verify error: {e}")
            return False