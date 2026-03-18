from flask import Flask, render_template, request, json
from cipher.caesar import CaesarCipher
from cipher.vigenere.vigenere_cipher import VigenereCipher
from cipher.railfence.railfence_cipher import RailFenceCipher
from cipher.playfair.playfair_cipher import PlayfairCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)

# router routes for home page
@app.route("/")
def home():
    return render_template('index.html')

# ----------------- CAESAR ROUTES -----------------
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    return render_template('caesar.html', encrypt_result=encrypted_text, plain_text=text, plain_key=key)

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    return render_template('caesar.html', decrypt_result=decrypted_text, cipher_text=text, cipher_key=key)

# ----------------- VIGENERE ROUTES -----------------
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/vigenere_encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    cipher = VigenereCipher()
    encrypted_text = cipher.encrypt_text(text, key)
    return render_template('vigenere.html', encrypt_result=encrypted_text, plain_text=text, plain_key=key)

@app.route("/vigenere_decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    cipher = VigenereCipher()
    decrypted_text = cipher.decrypt_text(text, key)
    return render_template('vigenere.html', decrypt_result=decrypted_text, cipher_text=text, cipher_key=key)

# ----------------- RAIL FENCE ROUTES -----------------
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/railfence_encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    cipher = RailFenceCipher()
    encrypted_text = cipher.rail_fence_encrypt(text, key)
    return render_template('railfence.html', encrypt_result=encrypted_text, plain_text=text, plain_key=key)

@app.route("/railfence_decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    cipher = RailFenceCipher()
    decrypted_text = cipher.rail_fence_decrypt(text, key)
    return render_template('railfence.html', decrypt_result=decrypted_text, cipher_text=text, cipher_key=key)

# ----------------- PLAYFAIR ROUTES -----------------
@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

@app.route("/playfair_encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    cipher = PlayfairCipher()
    encrypted_text = cipher.playfair_encrypt(text, key)
    return render_template('playfair.html', encrypt_result=encrypted_text, plain_text=text, plain_key=key)

@app.route("/playfair_decrypt", methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    cipher = PlayfairCipher()
    decrypted_text = cipher.playfair_decrypt(text, key)
    return render_template('playfair.html', decrypt_result=decrypted_text, cipher_text=text, cipher_key=key)

# ----------------- TRANSPOSITION ROUTES -----------------
@app.route("/transposition")
def transposition():
    return render_template('transposition.html')

@app.route("/transposition_encrypt", methods=['POST'])
def transposition_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    cipher = TranspositionCipher()
    encrypted_text = cipher.encrypt(text, key)
    return render_template('transposition.html', encrypt_result=encrypted_text, plain_text=text, plain_key=key)

@app.route("/transposition_decrypt", methods=['POST'])
def transposition_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    cipher = TranspositionCipher()
    decrypted_text = cipher.decrypt(text, key)
    return render_template('transposition.html', decrypt_result=decrypted_text, cipher_text=text, cipher_key=key)

# main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)