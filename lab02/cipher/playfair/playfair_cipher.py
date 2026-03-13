import re

class PlayfairCipher:
    def __init__(self):
        pass

    # Hàm tạo ma trận 5x5 theo yêu cầu 2.5.4
    def create_matrix(self, key):
        key = re.sub(r'[^A-Z]', '', key.upper().replace('J', 'I'))
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix_stuff = ""
        
        # Thêm các ký tự từ key vào chuỗi ma trận
        for char in key:
            if char not in matrix_stuff:
                matrix_stuff += char
        
        # Thêm các ký tự còn lại của bảng chữ cái
        for char in alphabet:
            if char not in matrix_stuff:
                matrix_stuff += char
                
        # Chuyển chuỗi 25 ký tự thành ma trận 5x5
        return [list(matrix_stuff[i:i+5]) for i in range(0, 25, 5)]

    def find_position(self, matrix, char):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
        return None

    def playfair_encrypt(self, plain_text, key):
        matrix = self.create_matrix(key)
        # Chuẩn hóa văn bản
        text = re.sub(r'[^A-Z]', '', plain_text.upper().replace('J', 'I'))
        
        prepared_text = ""
        i = 0
        while i < len(text):
            a = text[i]
            b = text[i+1] if i+1 < len(text) else 'X'
            if a == b:
                prepared_text += a + 'X'
                i += 1
            else:
                prepared_text += a + b
                i += 2
        if len(prepared_text) % 2 != 0:
            prepared_text += 'X'

        result = ""
        for i in range(0, len(prepared_text), 2):
            r1, c1 = self.find_position(matrix, prepared_text[i])
            r2, c2 = self.find_position(matrix, prepared_text[i+1])
            if r1 == r2:
                result += matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
            elif c1 == c2:
                result += matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
            else:
                result += matrix[r1][c2] + matrix[r2][c1]
        return result

    def playfair_decrypt(self, cipher_text, key):
        matrix = self.create_matrix(key)
        text = cipher_text.upper()
        result = ""
        for i in range(0, len(text), 2):
            r1, c1 = self.find_position(matrix, text[i])
            r2, c2 = self.find_position(matrix, text[i+1])
            if r1 == r2:
                result += matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
            elif c1 == c2:
                result += matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
            else:
                result += matrix[r1][c2] + matrix[r2][c1]
        return result