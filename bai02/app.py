# Bai 2.5.6: Giao dien web Flask
# Bai 3.5.1: API Caesar cho ung dung desktop
# Hoc vien: Le Hoang Huy - MSHV: 2410060274

from flask import Flask, render_template, request, jsonify

from caesar_cipher import CaesarCipher
from playfair_cipher import PlayfairCipher

app = Flask(__name__)


# Giao dien web Caesar va Playfair
@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    input_text = ""
    cipher_type = "caesar"
    action = "encrypt"
    shift = 3
    key = "SECURITY"

    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        cipher_type = request.form.get("cipher_type", "caesar")
        action = request.form.get("action", "encrypt")
        shift = int(request.form.get("shift", 3))
        key = request.form.get("key", "SECURITY")

        if cipher_type == "caesar":
            cipher = CaesarCipher(shift)

            if action == "encrypt":
                result = cipher.encrypt(input_text)
            else:
                result = cipher.decrypt(input_text)

        elif cipher_type == "playfair":
            cipher = PlayfairCipher(key)

            if action == "encrypt":
                result = cipher.encrypt(input_text)
            else:
                result = cipher.decrypt(input_text)

    return render_template(
        "index.html",
        result=result,
        input_text=input_text,
        cipher_type=cipher_type,
        action=action,
        shift=shift,
        key=key,
    )


# API ma hoa Caesar
@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Du lieu phai la JSON."}), 400

    message = data.get("plain_text")
    key = data.get("key")

    if not isinstance(message, str):
        return jsonify({"error": "plain_text phai la chuoi."}), 400

    try:
        shift = int(str(key))
    except (TypeError, ValueError):
        return jsonify({"error": "key phai la so nguyen."}), 400

    cipher = CaesarCipher(shift)
    encrypted_message = cipher.encrypt(message)

    return jsonify({
        "encrypted_message": encrypted_message
    })


# API giai ma Caesar
@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Du lieu phai la JSON."}), 400

    message = data.get("cipher_text")
    key = data.get("key")

    if not isinstance(message, str):
        return jsonify({"error": "cipher_text phai la chuoi."}), 400

    try:
        shift = int(str(key))
    except (TypeError, ValueError):
        return jsonify({"error": "key phai la so nguyen."}), 400

    cipher = CaesarCipher(shift)
    decrypted_message = cipher.decrypt(message)

    return jsonify({
        "decrypted_message": decrypted_message
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)