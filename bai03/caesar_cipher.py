# Bai 3.5.1: Ung dung desktop Caesar goi API Flask
# Le Hoang Huy - MSHV: 2410060274

import sys
import requests

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.api_url = "http://127.0.0.1:5000/api/caesar"

        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def get_key(self):
        try:
            return int(self.ui.txt_key.text().strip())
        except ValueError:
            QMessageBox.warning(
                self,
                "Khóa không hợp lệ",
                "Vui lòng nhập khóa là số nguyên, ví dụ: 3."
            )
            return None

    def send_request(self, action, payload):
        try:
            response = requests.post(
                f"{self.api_url}/{action}",
                json=payload,
                timeout=10
            )

            data = response.json()

            if response.status_code != 200:
                QMessageBox.warning(
                    self,
                    "Lỗi API",
                    data.get("error", "Không xử lý được yêu cầu.")
                )
                return None

            return data

        except requests.exceptions.ConnectionError:
            QMessageBox.warning(
                self,
                "Không kết nối được",
                "Hãy chạy bai02/app.py trước khi mã hóa hoặc giải mã."
            )

        except requests.exceptions.Timeout:
            QMessageBox.warning(
                self,
                "Hết thời gian chờ",
                "API chưa phản hồi. Vui lòng kiểm tra rồi thử lại."
            )

        except (requests.exceptions.RequestException, ValueError):
            QMessageBox.warning(
                self,
                "Lỗi phản hồi",
                "Không nhận được phản hồi JSON hợp lệ từ API."
            )

        return None

    def call_api_encrypt(self):
        key = self.get_key()

        if key is None:
            return

        plain_text = self.ui.txt_plain_text.toPlainText()

        if not plain_text.strip():
            QMessageBox.warning(
                self,
                "Thiếu nội dung",
                "Vui lòng nhập bản rõ cần mã hóa."
            )
            return

        data = self.send_request(
            "encrypt",
            {
                "plain_text": plain_text,
                "key": key
            }
        )

        if data is not None:
            self.ui.txt_cipher_text.setPlainText(
                data["encrypted_message"]
            )

            QMessageBox.information(
                self,
                "Thành công",
                "Mã hóa Caesar thành công."
            )

    def call_api_decrypt(self):
        key = self.get_key()

        if key is None:
            return

        cipher_text = self.ui.txt_cipher_text.toPlainText()

        if not cipher_text.strip():
            QMessageBox.warning(
                self,
                "Thiếu nội dung",
                "Vui lòng nhập bản mã cần giải mã."
            )
            return

        data = self.send_request(
            "decrypt",
            {
                "cipher_text": cipher_text,
                "key": key
            }
        )

        if data is not None:
            self.ui.txt_plain_text.setPlainText(
                data["decrypted_message"]
            )

            QMessageBox.information(
                self,
                "Thành công",
                "Giải mã Caesar thành công."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())