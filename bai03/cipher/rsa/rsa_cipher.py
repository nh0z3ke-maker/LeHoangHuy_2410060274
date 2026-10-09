# Bai 3.5.2: Xu ly mat ma RSA
# Le Hoang Huy - MSHV: 2410060274

from pathlib import Path

import rsa


class RSACipher:
    def __init__(self):
        self.keys_dir = Path(__file__).resolve().parent / "keys"
        self.keys_dir.mkdir(parents=True, exist_ok=True)

        self.public_key_path = self.keys_dir / "publicKey.pem"
        self.private_key_path = self.keys_dir / "privateKey.pem"

    def generate_keys(self):
        # rsa.newkeys tra ve khoa cong khai truoc, khoa rieng sau.
        public_key, private_key = rsa.newkeys(1024)

        self.public_key_path.write_bytes(
            public_key.save_pkcs1("PEM")
        )
        self.private_key_path.write_bytes(
            private_key.save_pkcs1("PEM")
        )

        return public_key, private_key

    def load_keys(self):
        if (
            not self.public_key_path.exists()
            or not self.private_key_path.exists()
        ):
            raise FileNotFoundError(
                "Chua co khoa RSA. Hay tao khoa truoc."
            )

        public_key = rsa.PublicKey.load_pkcs1(
            self.public_key_path.read_bytes()
        )
        private_key = rsa.PrivateKey.load_pkcs1(
            self.private_key_path.read_bytes()
        )

        return public_key, private_key

    def encrypt(self, message, public_key):
        message_bytes = message.encode("utf-8")

        # RSA PKCS#1 v1.5 can 11 byte cho padding.
        max_bytes = rsa.common.byte_size(public_key.n) - 11

        if len(message_bytes) > max_bytes:
            raise ValueError(
                f"Noi dung vuot qua {max_bytes} byte UTF-8. "
                "Hay nhap thong diep ngan hon."
            )

        return rsa.encrypt(message_bytes, public_key)

    def decrypt(self, ciphertext, private_key):
        message_bytes = rsa.decrypt(ciphertext, private_key)
        return message_bytes.decode("utf-8")

    def sign(self, message, private_key):
        return rsa.sign(
            message.encode("utf-8"),
            private_key,
            "SHA-256"
        )

    def verify(self, message, signature, public_key):
        try:
            rsa.verify(
                message.encode("utf-8"),
                signature,
                public_key
            )
            return True

        except rsa.VerificationError:
            return False