import sys
from PyQt5 import QtWidgets
from ui.ecc import Ui_MainWindow
import requests

API_URL = "http://127.0.0.1:5000/api/ecc"

class ECCApp:
    def __init__(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        
        # Connect signals
        self.ui.btnGenerateKey.clicked.connect(self.generate_key)
        self.ui.btnSign.clicked.connect(self.sign_message)
        self.ui.btnVerify.clicked.connect(self.verify_message)

    def generate_key(self):
        try:
            res = requests.post(f"{API_URL}/generate_keys")
            if res.status_code == 200:
                self.ui.txtInformation.setText("✓ ECC Keys generated!")
            else:
                self.ui.txtInformation.setText("✗ Error")
        except Exception as e:
            self.ui.txtInformation.setText(f"Error: {str(e)}")

    def sign_message(self):
        try:
            msg = self.ui.txtInformation.toPlainText()
            if not msg:
                self.ui.txtInformation.setText("⚠ Enter message")
                return
            res = requests.post(f"{API_URL}/sign", json={"message": msg})
            if res.status_code == 200:
                self.ui.txtSignature.setText(res.json().get('signature'))
                self.ui.txtInformation.setText("✓ Signed")
        except Exception as e:
            self.ui.txtInformation.setText(f"Error: {str(e)}")

    def verify_message(self):
        try:
            msg = self.ui.txtInformation.toPlainText()
            sig = self.ui.txtSignature.toPlainText()
            if not msg or not sig:
                self.ui.txtInformation.setText("⚠ Enter both")
                return
            res = requests.post(f"{API_URL}/verify", json={"message": msg, "signature": sig})
            if res.status_code == 200:
                valid = res.json().get('valid')
                self.ui.txtInformation.setText(f"{'✓ VALID' if valid else '✗ INVALID'}")
        except Exception as e:
            self.ui.txtInformation.setText(f"Error: {str(e)}")

    def show(self):
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ECCApp()
    window.show()
    sys.exit(app.exec_())