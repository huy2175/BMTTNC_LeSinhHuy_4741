class VigenereCipher:
    def __init__(self):
        pass

    def encrypt_text(self, text, key):
        if not text or not key: return ""
        text = text.upper()
        key = key.upper()
        encrypted_text = ""
        key_index = 0
        
        for char in text:
            if char.isalpha():
                # Tính độ dịch chuyển dựa trên ký tự của key
                shift = ord(key[key_index % len(key)]) - ord('A')
                # Công thức: En(x) = (x + n) mod 26
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                encrypted_text += new_char
                key_index += 1
            else:
                encrypted_text += char
        return encrypted_text

    def decrypt_text(self, text, key):
        if not text or not key: return ""
        text = text.upper()
        key = key.upper()
        decrypted_text = ""
        key_index = 0
        
        for char in text:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
                # Công thức giải mã: Dn(x) = (x - n + 26) mod 26
                new_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
                decrypted_text += new_char
                key_index += 1
            else:
                decrypted_text += char
        return decrypted_text