import sys

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from ui.rsa import Ui_MainWindow


API_URL = "http://127.0.0.1:5000/api/rsa"


class RSAApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_gen_keys.clicked.connect(self.generate_keys)
        self.ui.btn_encrypt.clicked.connect(self.encrypt)
        self.ui.btn_decrypt.clicked.connect(self.decrypt)
        self.ui.btn_sign.clicked.connect(self.sign)
        self.ui.btn_verify.clicked.connect(self.verify)

    def call_api(self, endpoint, payload=None):
        try:
            url = f"{API_URL}/{endpoint}"

            if payload is None:
                response = requests.get(url, timeout=30)
            else:
                response = requests.post(url, json=payload, timeout=10)

            data = response.json()

            if not response.ok:
                raise ValueError(data.get("error", "API xử lý thất bại."))

            return data

        except requests.exceptions.ConnectionError:
            QMessageBox.warning(
                self,
                "Lỗi kết nối",
                "Không kết nối được API. Hãy chạy api.py trước.",
            )
        except requests.exceptions.Timeout:
            QMessageBox.warning(self, "Hết thời gian", "API phản hồi quá chậm.")
        except (requests.exceptions.RequestException, ValueError) as error:
            QMessageBox.warning(self, "Lỗi", str(error))

        return None

    def require_text(self, text, message):
        if not text.strip():
            QMessageBox.warning(self, "Thiếu dữ liệu", message)
            return False
        return True

    def generate_keys(self):
        data = self.call_api("generate_keys")
        if data is not None:
            # Cặp khóa mới thay thế cặp khóa cũ.
            self.ui.txt_cipher_text.clear()
            self.ui.txt_sign.clear()
            QMessageBox.information(
                self,
                "Tạo khóa",
                data.get("message", "Tạo và lưu cặp khóa RSA thành công."),
            )

    def encrypt(self):
        message = self.ui.txt_plain_text.toPlainText()
        if not self.require_text(message, "Hãy nhập bản rõ cần mã hóa."):
            return

        data = self.call_api(
            "encrypt",
            {"message": message, "key_type": "public"},
        )
        if data is not None:
            self.ui.txt_cipher_text.setPlainText(data["encrypted_message"])
            QMessageBox.information(self, "Mã hóa", "Mã hóa RSA thành công.")

    def decrypt(self):
        ciphertext = self.ui.txt_cipher_text.toPlainText().strip()
        if not self.require_text(ciphertext, "Hãy nhập bản mã cần giải mã."):
            return

        data = self.call_api(
            "decrypt",
            {"ciphertext": ciphertext, "key_type": "private"},
        )
        if data is not None:
            self.ui.txt_plain_text.setPlainText(data["decrypted_message"])
            QMessageBox.information(self, "Giải mã", "Giải mã RSA thành công.")

    def sign(self):
        message = self.ui.txt_info.toPlainText()
        if not self.require_text(message, "Hãy nhập thông điệp cần ký."):
            return

        data = self.call_api("sign", {"message": message})
        if data is not None:
            self.ui.txt_sign.setPlainText(data["signature"])
            QMessageBox.information(self, "Chữ ký số", "Ký thông điệp thành công.")

    def verify(self):
        message = self.ui.txt_info.toPlainText()
        signature = self.ui.txt_sign.toPlainText().strip()

        if not self.require_text(message, "Hãy nhập thông điệp cần xác minh."):
            return
        if not self.require_text(signature, "Hãy nhập chữ ký cần xác minh."):
            return

        data = self.call_api(
            "verify",
            {"message": message, "signature": signature},
        )
        if data is not None:
            if data["is_verified"]:
                QMessageBox.information(
                    self,
                    "Xác minh chữ ký",
                    "Chữ ký hợp lệ. Thông điệp khớp với chữ ký.",
                )
            else:
                QMessageBox.warning(
                    self,
                    "Xác minh chữ ký",
                    "Chữ ký không hợp lệ đối với thông điệp và khóa hiện tại.",
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSAApp()
    window.show()
    sys.exit(app.exec_())