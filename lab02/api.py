from flask import Flask, request, jsonify
from cipher.caesar.caesar_cipher import CaesarCipher
from cipher.vigenere.vigenere_cipher import VigenereCipher
# SỬA DÒNG NÀY: Trỏ trực tiếp vào file railfence_cipher.py
from cipher.railfence.railfence_cipher import RailFenceCipher
from cipher.playfair.playfair_cipher import PlayfairCipher
from cipher.transposition import TranspositionCipher
app = Flask(__name__)

# Khởi tạo đối tượng cho các thuật toán
caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
playfair_cipher = PlayfairCipher()
transposition_cipher = TranspositionCipher()
# ----------------- CAESAR ENDPOINTS -----------------
@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.get_json()
    text = data.get('text', "")
    key = int(data.get('key', 0))
    encrypted_text = caesar_cipher.encrypt_text(text, key)
    return jsonify({"encrypted_text": encrypted_text})

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.get_json()
    text = data.get('text', "")
    key = int(data.get('key', 0))
    decrypted_text = caesar_cipher.decrypt_text(text, key)
    return jsonify({"decrypted_text": decrypted_text})

# ----------------- VIGENERE ENDPOINTS -----------------
@app.route("/api/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    data = request.get_json()
    text = data.get('text', "")
    key = data.get('key', "")
    encrypted_text = vigenere_cipher.encrypt_text(text, key)
    return jsonify({"encrypted_text": encrypted_text})

@app.route("/api/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    data = request.get_json()
    text = data.get('text', "")
    key = data.get('key', "")
    decrypted_text = vigenere_cipher.decrypt_text(text, key)
    return jsonify({"decrypted_text": decrypted_text})

# ----------------- RAIL FENCE ENDPOINTS (Bài 2.5.3) -----------------
@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    data = request.get_json()
    # Sử dụng .get() để tránh lỗi 500 nếu thiếu dữ liệu
    # Accept either 'plain_text' or 'text' for convenience
    plain_text = data.get('plain_text') or data.get('text', "")
    key = int(data.get('key', 0))
    encrypted_text = railfence_cipher.rail_fence_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    data = request.get_json()
    # Accept common field names: 'cipher_text', 'text', or (mistakenly) 'plain_text'
    cipher_text = data.get('cipher_text') or data.get('text') or data.get('plain_text', "")
    key = int(data.get('key', 0))
    decrypted_text = railfence_cipher.rail_fence_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})
#---------------------------------playfair_cipher-----------------
@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix():
    data = request.get_json()
    key = data.get('key', "")
    # Gọi hàm tạo ma trận từ class
    matrix = playfair_cipher.create_matrix(key)
    return jsonify({'matrix': matrix})

@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    data = request.get_json()
    plain_text = data.get('plain_text', "")
    key = data.get('key', "")
    encrypted_text = playfair_cipher.playfair_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    data = request.get_json()
    cipher_text = data.get('cipher_text', "")
    key = data.get('key', "")
    decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

# ----------------- TRANSPOSITION ENDPOINTS (2.5.5) -----------------

@app.route('/api/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    data = request.get_json()
    plain_text = data.get('plain_text', "")
    key = int(data.get('key', 0))
    res = transposition_cipher.encrypt(plain_text, key)
    return jsonify({'encrypted_text': res})

@app.route('/api/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    data = request.get_json()
    cipher_text = data.get('cipher_text', "")
    key = int(data.get('key', 0))
    res = transposition_cipher.decrypt(cipher_text, key)
    return jsonify({'decrypted_text': res})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)