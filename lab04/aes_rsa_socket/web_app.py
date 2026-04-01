from flask import Flask, request, jsonify, render_template
import socket
import threading
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

app = Flask(__name__, template_folder='templates')

server_address = ('127.0.0.1', 12345)
client_socket = None
server_public_key = None
receive_thread = None
message_queue = []
running = False
lock = threading.Lock()

HTML = """
<!doctype html>
<html lang='en'>
  <head>
    <meta charset='utf-8'>
    <title>AES-RSA Socket Web UI</title>
    <style>
      body { font-family: Arial, sans-serif; padding: 20px; }
      #messages { width: 100%; height: 300px; border: 1px solid #ccc; overflow: auto; margin-bottom: 8px; padding: 6px; white-space: pre-wrap; }
      #status { margin-bottom: 12px; }
      button { margin-right: 8px; }
    </style>
  </head>
  <body>
    <h2>AES-RSA Socket Web UI</h2>
    <div id='status'>Status: <span id='statusText'>Disconnected</span></div>
    <div id='messages'></div>
    <input id='message' style='width:70%;' placeholder='Type message...' />
    <button onclick='sendMessage()'>Send</button>
    <button onclick='connectServer()'>Connect</button>

    <script>
      async function connectServer() {
        try {
          const res = await fetch('/connect');
          const j = await res.json();
          document.getElementById('statusText').textContent = j.status;
          alert(j.message);
        } catch (err) {
          document.getElementById('statusText').textContent = 'Error';
          alert('Connect failed: ' + err);
          console.error('Connect call exception', err);
        }
      }

      async function sendMessage() {
        const msg = document.getElementById('message').value;
        if (!msg) return;
        await fetch('/send', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({message: msg}) });
        document.getElementById('message').value = '';
      }

      async function poll() {
        const res = await fetch('/poll');
        const j = await res.json();
        if (j.messages.length) {
          const box = document.getElementById('messages');
          for (let m of j.messages) {
            box.textContent += m + '\n';
          }
          box.scrollTop = box.scrollHeight;
        }
      }

      setInterval(poll, 500);
    </script>
  </body>
</html>
"""


def receive_loop():
    global running, client_socket
    while running and client_socket:
        try:
            header = client_socket.recv(4)
            if not header or len(header) < 4:
                break
            length = int.from_bytes(header, 'big')
            data = b''
            while len(data) < length:
                chunk = client_socket.recv(length - len(data))
                if not chunk:
                    break
                data += chunk
            if not data:
                break
            text = data.decode(errors='replace')
            with lock:
                message_queue.append(text)
        except Exception as e:
            with lock:
                message_queue.append(f"[ERROR] Receive loop error: {e}")
            break

    running = False
    if client_socket:
        try:
            client_socket.close()
        except Exception:
            pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/connect')
def connect():
    global client_socket, server_public_key, receive_thread, running

    print('[WEBAPP] /connect called, running=', running, 'server_address=', server_address)

    if running:
        return jsonify(status='Connected', message='Already connected')

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)
        client_socket.connect(server_address)
        client_socket.settimeout(None)
        print('[WEBAPP] socket connect success')

        raw = client_socket.recv(4)
        if len(raw) < 4:
            raise RuntimeError('Unable to read public key length from server')
        key_len = int.from_bytes(raw, 'big')
        key_data = b''
        while len(key_data) < key_len:
            chunk = client_socket.recv(key_len - len(key_data))
            if not chunk:
                break
            key_data += chunk

        if len(key_data) != key_len:
            raise RuntimeError('Public key data truncated')

        server_public_key = RSA.import_key(key_data)

        running = True
        receive_thread = threading.Thread(target=receive_loop, daemon=True)
        receive_thread.start()

        return jsonify(status='Connected', message='Connected to server')

    except Exception as e:
        import traceback
        traceback.print_exc()
        client_socket = None
        running = False
        return jsonify(status='Error', message=str(e))


@app.route('/send', methods=['POST'])
def send():
    global client_socket, server_public_key
    if not client_socket or not running or not server_public_key:
        return jsonify(success=False, message='Not connected')

    data = request.get_json() or {}
    msg = data.get('message', '').strip()
    if not msg:
        return jsonify(success=False, message='Empty message')

    try:
        session_key = get_random_bytes(32)
        aes_cipher = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = aes_cipher.encrypt_and_digest(msg.encode('utf-8'))

        rsa_cipher = PKCS1_OAEP.new(server_public_key)
        encrypted_key = rsa_cipher.encrypt(session_key)

        payload = {
            'encrypted_key': encrypted_key.hex(),
            'nonce': aes_cipher.nonce.hex(),
            'ciphertext': ciphertext.hex(),
            'tag': tag.hex()
        }
        bpayload = json.dumps(payload).encode('utf-8')

        client_socket.sendall(len(bpayload).to_bytes(4, 'big') + bpayload)
        return jsonify(success=True)

    except Exception as e:
        return jsonify(success=False, message=str(e))


@app.route('/poll')
def poll():
    global message_queue
    with lock:
        messages = list(message_queue)
        message_queue.clear()
    return jsonify(messages=messages)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
