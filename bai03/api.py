# Bai 3.5.2: API Flask cho RSA
# Le Hoang Huy - MSHV: 2410060274

import rsa

from flask import Flask, request, jsonify
from cipher.rsa.rsa_cipher import RSACipher

app = Flask(__name__)
rsa_cipher = RSACipher()


def get_json_data():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        raise ValueError("Du lieu phai la mot doi tuong JSON.")

    return data


def get_text(data, field):
    value = data.get(field)

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} phai la chuoi khong rong.")

    return value


@app.errorhandler(FileNotFoundError)
def handle_missing_keys(error):
    return jsonify({"error": str(error)}), 400


@app.errorhandler(ValueError)
def handle_invalid_data(error):
    return jsonify({"error": str(error)}), 400


@app.errorhandler(OverflowError)
def handle_long_message(error):
    return jsonify({
        "error": "Thong diep qua dai de ma hoa RSA."
    }), 400


@app.errorhandler(rsa.DecryptionError)
def handle_decryption_error(error):
    return jsonify({
        "error": "Khong giai ma duoc. Kiem tra ban ma va khoa RSA."
    }), 400


# Tao cap khoa RSA va luu vao thu muc keys
@app.route("/api/rsa/generate_keys", methods=["GET"])
def generate_keys():
    rsa_cipher.generate_keys()

    return jsonify({
        "message": "Tao va luu cap khoa RSA thanh cong."
    })


# Ma hoa bang khoa cong khai
@app.route("/api/rsa/encrypt", methods=["POST"])
def encrypt_message():
    data = get_json_data()
    message = get_text(data, "message")

    if data.get("key_type", "public") != "public":
        raise ValueError("Ma hoa phai su dung khoa public.")

    public_key, _ = rsa_cipher.load_keys()
    ciphertext = rsa_cipher.encrypt(message, public_key)

    return jsonify({
        "encrypted_message": ciphertext.hex()
    })


# Giai ma bang khoa rieng
@app.route("/api/rsa/decrypt", methods=["POST"])
def decrypt_message():
    data = get_json_data()
    ciphertext_hex = get_text(data, "ciphertext")

    if data.get("key_type", "private") != "private":
        raise ValueError("Giai ma phai su dung khoa private.")

    ciphertext = bytes.fromhex(ciphertext_hex)
    _, private_key = rsa_cipher.load_keys()

    message = rsa_cipher.decrypt(ciphertext, private_key)

    return jsonify({
        "decrypted_message": message
    })


# Tao chu ky so bang khoa rieng
@app.route("/api/rsa/sign", methods=["POST"])
def sign_message():
    data = get_json_data()
    message = get_text(data, "message")

    _, private_key = rsa_cipher.load_keys()
    signature = rsa_cipher.sign(message, private_key)

    return jsonify({
        "signature": signature.hex()
    })


# Xac minh chu ky bang khoa cong khai
@app.route("/api/rsa/verify", methods=["POST"])
def verify_signature():
    data = get_json_data()
    message = get_text(data, "message")
    signature_hex = get_text(data, "signature")

    signature = bytes.fromhex(signature_hex)
    public_key, _ = rsa_cipher.load_keys()

    is_verified = rsa_cipher.verify(
        message,
        signature,
        public_key
    )

    return jsonify({
        "is_verified": is_verified
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)