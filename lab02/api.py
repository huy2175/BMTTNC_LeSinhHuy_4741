from flask import Flask, request, jsonify
from cipher.caesar.caesar_cipher import CaesarCipher
from cipher.vigenere.vigenere_cipher import VigenereCipher

app = Flask(__name__)

# Khởi tạo đối tượng cho các thuật toán
caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)