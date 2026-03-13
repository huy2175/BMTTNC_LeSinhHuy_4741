class RailFenceCipher: # Chú ý: Viết hoa chữ R, F và C
    def __init__(self):
        pass

    def rail_fence_encrypt(self, plain_text, key):
        fence = [[] for _ in range(key)]
        rail = 0
        direction = 1
        for char in plain_text:
            fence[rail].append(char)
            rail += direction
            if rail == 0 or rail == key - 1:
                direction = -direction
        return "".join(["".join(rail) for rail in fence])

    def rail_fence_decrypt(self, cipher_text, key):
        fence = [[None for _ in range(len(cipher_text))] for _ in range(key)]
        rail = 0
        direction = 1
        for i in range(len(cipher_text)):
            fence[rail][i] = '*'
            rail += direction
            if rail == 0 or rail == key - 1:
                direction = -direction
        index = 0
        for r in range(key):
            for c in range(len(cipher_text)):
                if fence[r][c] == '*' and index < len(cipher_text):
                    fence[r][c] = cipher_text[index]
                    index += 1
        result = []
        rail = 0
        direction = 1
        for i in range(len(cipher_text)):
            result.append(fence[rail][i])
            rail += direction
            if rail == 0 or rail == key - 1:
                direction = -direction
        return "".join(result)