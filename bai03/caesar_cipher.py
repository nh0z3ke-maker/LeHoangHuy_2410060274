import sys
import requests

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow


class CaesarCipherWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_encrypt.clicked.connect(self.encrypt_text)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_text)

    def get_key(self):
        try:
            return int(self.ui.txt_key.text())
        except ValueError:
            raise ValueError("Khóa phải là một số nguyên.")

    def encrypt_text(self):
        try:
            plain_text = self.ui.txt_plain_text.toPlainText()
            key = self.get_key()

            response = requests.post(
                "http://127.0.0.1:5000/api/caesar/encrypt",
                json={
                    "plain_text": plain_text,
                    "key": key
                },
                timeout=5
            )

            response.raise_for_status()
            result = response.json()["encrypted_message"]
            self.ui.txt_cipher_text.setPlainText(result)

        except Exception as error:
            QMessageBox.critical(self, "Lỗi mã hóa", str(error))

    def decrypt_text(self):
        try:
            cipher_text = self.ui.txt_cipher_text.toPlainText()
            key = self.get_key()

            response = requests.post(
                "http://127.0.0.1:5000/api/caesar/decrypt",
                json={
                    "cipher_text": cipher_text,
                    "key": key
                },
                timeout=5
            )

            response.raise_for_status()
            result = response.json()["decrypted_message"]
            self.ui.txt_plain_text.setPlainText(result)

        except Exception as error:
            QMessageBox.critical(self, "Lỗi giải mã", str(error))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaesarCipherWindow()
    window.show()
    sys.exit(app.exec_())