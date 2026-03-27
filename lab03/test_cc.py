import sys
from PyQt5 import QtWidgets

print("🔧 Starting test...", flush=True)

try:
    from ui.ecc import Ui_MainWindow
    print("✓ Import successful!", flush=True)
except Exception as e:
    print(f"✗ Import failed: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("🚀 Creating app...", flush=True)
app = QtWidgets.QApplication(sys.argv)
print("✓ App created", flush=True)

window = QtWidgets.QMainWindow()
print("✓ MainWindow created", flush=True)

ui = Ui_MainWindow()
print("✓ Ui_MainWindow created", flush=True)

ui.setupUi(window)
print("✓ UI setup complete", flush=True)

window.show()
print("✓ Window shown - Check Alt+Tab!", flush=True)
window.raise_()
window.activateWindow()

import time
time.sleep(3)

print("🔄 Starting event loop...", flush=True)
sys.exit(app.exec_())