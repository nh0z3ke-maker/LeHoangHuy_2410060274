# 2.5.6 - Tao giao dien web bang Flask

from flask import Flask, render_template, request

from caesar_cipher import CaesarCipher
from playfair_cipher import PlayfairCipher

app = Flask(__name__)


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

        if cipher_type == "playfair":
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

@app.post("/api/caesar/encrypt")
def api_caesar_encrypt():
    data = request.get_json(silent=True) or {}

    plain_text = data.get("plain_text", "")
    key = int(data.get("key", 3))

    cipher = CaesarCipher(key)
    encrypted_message = cipher.encrypt(plain_text)

    return {
        "encrypted_message": encrypted_message
    }


@app.post("/api/caesar/decrypt")
def api_caesar_decrypt():
    data = request.get_json(silent=True) or {}

    cipher_text = data.get("cipher_text", "")
    key = int(data.get("key", 3))

    cipher = CaesarCipher(key)
    decrypted_message = cipher.decrypt(cipher_text)

    return {
        "decrypted_message": decrypted_message
    }

@app.post("/api/playfair/encrypt")
def api_playfair_encrypt():
    data = request.get_json(silent=True) or {}
    plain_text = data.get("plain_text", "")
    key = data.get("key", "SECURITY")

    cipher = PlayfairCipher(key)
    encrypted_message = cipher.encrypt(plain_text)

    return {"encrypted_message": encrypted_message}


@app.post("/api/playfair/decrypt")
def api_playfair_decrypt():
    data = request.get_json(silent=True) or {}
    cipher_text = data.get("cipher_text", "")
    key = data.get("key", "SECURITY")

    cipher = PlayfairCipher(key)
    decrypted_message = cipher.decrypt(cipher_text)

    return {"decrypted_message": decrypted_message}
if __name__ == "__main__":
    app.run(debug=True)