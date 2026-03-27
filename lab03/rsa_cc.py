import sys
from PyQt5 import QtWidgets
from ui.rsa import Ui_MainWindow  # Import từ file ui vừa sinh
import requests

API_URL = "http://127.0.0.1:5000/api/rsa"

class RSAApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Gán sự kiện cho các button
        self.btnGenerateKey.clicked.connect(self.generate_key)
        self.btnEncrypt.clicked.connect(self.encrypt_message)
        self.btnDecrypt.clicked.connect(self.decrypt_message)
        self.btnSign.clicked.connect(self.sign_message)
        self.btnVerify.clicked.connect(self.verify_message)

    def generate_key(self):
        try:
            res = requests.post(f"{API_URL}/generate_keys")
            if res.status_code == 200:
                self.txtInformation.setText("Keys generated successfully!\nCheck folder cipher/rsa/keys")
            else:
                self.txtInformation.setText("Error generating keys")
        except Exception as e:
            self.txtInformation.setText(f"Error: {str(e)}")

    def encrypt_message(self):
        try:
            msg = self.txtPlainText.toPlainText()  # ✅ Sửa: txtInput → txtPlainText
            if not msg:
                self.txtInformation.setText("Please enter message")
                return
            res = requests.post(f"{API_URL}/encrypt", json={"message": msg})
            if res.status_code == 200:
                self.txtCipherText.setText(res.json().get('ciphertext'))  # ✅ Hiển thị vào txtCipherText
            else:
                self.txtInformation.setText("Encryption failed")
        except Exception as e:
            self.txtInformation.setText(f"Error: {str(e)}")

    def decrypt_message(self):
        try:
            cipher = self.txtPlainText.toPlainText()  # ✅ Nhập ciphertext từ txtPlainText
            if not cipher:
                self.txtInformation.setText("Please enter ciphertext")
                return
            res = requests.post(f"{API_URL}/decrypt", json={"ciphertext": cipher})
            if res.status_code == 200:
                self.txtCipherText.setText(res.json().get('message'))  # ✅ Hiển thị kết quả vào txtCipherText
            else:
                self.txtInformation.setText("Decryption failed")
        except Exception as e:
            self.txtInformation.setText(f"Error: {str(e)}")

    def sign_message(self):
        try:
            msg = self.txtPlainText.toPlainText()
            if not msg:
                self.txtInformation.setText("Please enter message")
                return
            res = requests.post(f"{API_URL}/sign", json={"message": msg})
            if res.status_code == 200:
                self.txtSignature.setText(res.json().get('signature'))  # ✅ Hiển thị signature vào txtSignature
            else:
                self.txtInformation.setText("Sign failed")
        except Exception as e:
            self.txtInformation.setText(f"Error: {str(e)}")

    def verify_message(self):
        try:
            # Nhập message ở txtPlainText và signature ở txtSignature
            msg = self.txtPlainText.toPlainText()
            signature = self.txtSignature.toPlainText()
            
            if not msg or not signature:
                self.txtInformation.setText("Please enter message and signature")
                return

            res = requests.post(f"{API_URL}/verify", json={"message": msg, "signature": signature})
            if res.status_code == 200:
                valid = res.json().get('valid')
                self.txtInformation.setText(f"Verification Result: {valid}")
            else:
                self.txtInformation.setText("Verify failed")
        except Exception as e:
            self.txtInformation.setText(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RSAApp()
    window.show()
    sys.exit(app.exec_())