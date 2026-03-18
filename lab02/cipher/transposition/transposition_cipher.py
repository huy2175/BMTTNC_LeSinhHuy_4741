import math

class TranspositionCipher:
    def __init__(self):
        pass

    def encrypt(self, text, key):
        # Tạo danh sách các cột rỗng
        ciphertext = [''] * key
        # Duyệt qua từng ký tự trong văn bản gốc
        for col in range(key):
            pointer = col
            while pointer < len(text):
                ciphertext[col] += text[pointer]
                pointer += key
        return ''.join(ciphertext)

    def decrypt(self, text, key):
        # Tính số cột cần thiết cho ma trận
        num_cols = math.ceil(len(text) / key)
        num_rows = key
        num_shaded_boxes = (num_cols * num_rows) - len(text)
        
        plaintext = [''] * num_cols
        col = 0
        row = 0
        
        for symbol in text:
            plaintext[col] += symbol
            col += 1
            # Nếu chạm đến cột cuối hoặc ô bị xám (shaded), quay lại hàng tiếp theo
            if (col == num_cols) or (col == num_cols - 1 and row >= num_rows - num_shaded_boxes):
                col = 0
                row += 1
        return ''.join(plaintext)