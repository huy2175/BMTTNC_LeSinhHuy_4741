from cipher.caesar.alphabet import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET

    def encrypt_text(self, text, key):
        if not text: return ""
        text = text.upper()
        encrypted_text = ""
        for char in text:
            if char in self.alphabet:
                index = self.alphabet.index(char)
                new_index = (index + key) % len(self.alphabet)
                encrypted_text += self.alphabet[new_index]
            else:
                encrypted_text += char
        return encrypted_text

    def decrypt_text(self, text, key):
        if not text: return ""
        # Giải mã là mã hóa với khóa đối nghịch
        return self.encrypt_text(text, -key)