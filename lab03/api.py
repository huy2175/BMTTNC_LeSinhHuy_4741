from flask import Flask, request, jsonify
from cipher.rsa import RSACipher
import os

app = Flask(__name__)
rsa_cipher = RSACipher()

@app.route('/api/rsa/generate_keys', methods=['POST'])
def generate_keys():
    try:
        rsa_cipher.generate_keys()
        return jsonify({'message': 'Keys generated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rsa/encrypt', methods=['POST'])
def encrypt():
    try:
        data = request.get_json()
        message = data.get('message')
        _, public_key = rsa_cipher.load_keys()
        ciphertext = rsa_cipher.encrypt(message, public_key)
        return jsonify({'ciphertext': ciphertext.hex()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rsa/decrypt', methods=['POST'])
def decrypt():
    try:
        data = request.get_json()
        ciphertext = bytes.fromhex(data.get('ciphertext'))
        private_key, _ = rsa_cipher.load_keys()
        message = rsa_cipher.decrypt(ciphertext, private_key)
        return jsonify({'message': message}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rsa/sign', methods=['POST'])
def sign():
    try:
        data = request.get_json()
        message = data.get('message')
        private_key, _ = rsa_cipher.load_keys()
        signature = rsa_cipher.sign(message, private_key)
        return jsonify({'signature': signature.hex()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rsa/verify', methods=['POST'])
def verify():
    try:
        data = request.get_json()
        message = data.get('message')
        signature = bytes.fromhex(data.get('signature'))
        _, public_key = rsa_cipher.load_keys()
        is_valid = rsa_cipher.verify(message, signature, public_key)
        return jsonify({'valid': is_valid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)