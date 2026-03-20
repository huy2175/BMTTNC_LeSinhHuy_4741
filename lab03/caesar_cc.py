import sys
import requests
import os
# Đảm bảo đường dẫn plugin cho PyQt5
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.getcwd(), 'platforms')

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow  # Import class từ file giao diện của bạn

class CaesarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Kết nối các nút bấm với hàm xử lý
        self.ui.btnEn.clicked.connect(self.process_encrypt)
        self.ui.btnDe.clicked.connect(self.process_decrypt)

    def process_encrypt(self):
        # Lấy dữ liệu (Dùng toPlainText cho QTextEdit, text cho QLineEdit)
        text = self.ui.ccPlain.toPlainText()
        key = self.ui.ccKey.text()
        
        if not text or not key:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản và khóa!")
            return

        try:
            # Gửi yêu cầu đến server api.py (Cổng 5000)
            payload = {"text": text, "key": int(key)}
            response = requests.post("http://127.0.0.1:5000/api/caesar/encrypt", json=payload)
            
            if response.status_code == 200:
                result = response.json().get('encrypted_text')
                self.ui.ccCipher.setPlainText(result)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối đến Server: {e}")

    def process_decrypt(self):
        text = self.ui.ccCipher.toPlainText()
        key = self.ui.ccKey.text()
        
        try:
            payload = {"text": text, "key": int(key)}
            response = requests.post("http://127.0.0.1:5000/api/caesar/decrypt", json=payload)
            if response.status_code == 200:
                result = response.json().get('decrypted_text')
                self.ui.ccPlain.setPlainText(result)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối đến Server: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaesarApp()
    window.show()
    sys.exit(app.exec_())