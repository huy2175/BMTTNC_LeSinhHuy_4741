from flask import Flask, request, jsonify
from flask_cors import CORS
from cipher.rsa import RSACipher
from cipher.ecc import ECCCipher
import os

app = Flask(__name__)
CORS(app)  # Cho phép GUI gọi API từ khác origin

# Khởi tạo cipher objects
rsa_cipher = RSACipher()
ecc_cipher = ECCCipher()

# ==================== RSA API ROUTES ====================

@app.route('/api/rsa/generate_keys', methods=['POST'])
def rsa_generate_keys():
    try:
        rsa_cipher.generate_keys()
        return jsonify({'message': 'RSA Keys generated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rsa/encrypt', methods=['POST'])
def rsa_encrypt():
    try:
        data = request.get_json()
        message = data.get('message')
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        _, public_key = rsa_cipher.load_keys()
        if not public_key:
            return jsonify({'error': 'Keys not found. Generate keys first.'}), 400
        
        ciphertext = rsa_cipher.encrypt(message, public_key)
        return jsonify({'ciphertext': ciphertext.hex()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rsa/decrypt', methods=['POST'])
def rsa_decrypt():
    try:
        data = request.get_json()
        ciphertext = data.get('ciphertext')
        if not ciphertext:
            return jsonify({'error': 'Ciphertext is required'}), 400
        
        ciphertext = bytes.fromhex(ciphertext)
        private_key, _ = rsa_cipher.load_keys()
        if not private_key:
            return jsonify({'error': 'Keys not found. Generate keys first.'}), 400
        
        message = rsa_cipher.decrypt(ciphertext, private_key)
        return jsonify({'message': message}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign():
    try:
        data = request.get_json()
        message = data.get('message')
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        private_key, _ = rsa_cipher.load_keys()
        if not private_key:
            return jsonify({'error': 'Keys not found. Generate keys first.'}), 400
        
        signature = rsa_cipher.sign(message, private_key)
        return jsonify({'signature': signature.hex()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify():
    try:
        data = request.get_json()
        message = data.get('message')
        signature = data.get('signature')
        
        if not message or not signature:
            return jsonify({'error': 'Message and signature are required'}), 400
        
        signature = bytes.fromhex(signature)
        _, public_key = rsa_cipher.load_keys()
        if not public_key:
            return jsonify({'error': 'Keys not found. Generate keys first.'}), 400
        
        is_valid = rsa_cipher.verify(message, signature, public_key)
        return jsonify({'valid': is_valid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ECC API ROUTES ====================

@app.route('/api/ecc/generate_keys', methods=['POST'])
def ecc_generate_keys():
    try:
        ecc_cipher.generate_keys()
        return jsonify({'message': 'ECC Keys generated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ecc/sign', methods=['POST'])
def ecc_sign():
    try:
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        private_key, _ = ecc_cipher.load_keys()
        if not private_key:
            return jsonify({'error': 'Keys not found. Generate keys first.'}), 400
        
        signature = ecc_cipher.sign(message)
        return jsonify({'signature': signature}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ecc/verify', methods=['POST'])
def ecc_verify():
    try:
        data = request.get_json()
        message = data.get('message')
        signature = data.get('signature')
        
        if not message or not signature:
            return jsonify({'error': 'Message and signature are required'}), 400
        
        _, public_key = ecc_cipher.load_keys()
        if not public_key:
            return jsonify({'error': 'Keys not found. Generate keys first.'}), 400
        
        is_valid = ecc_cipher.verify(message, signature)
        return jsonify({'valid': is_valid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'API Server is running'}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)