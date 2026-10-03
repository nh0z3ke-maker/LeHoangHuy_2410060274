# 2.5.1 - Ma hoa va giai ma Caesar Cipher


class CaesarCipher:
    def __init__(self, shift):
        self.shift = shift

    def encrypt(self, plaintext):
        ciphertext = ""

        for char in plaintext:
            if char.isalpha():
                base = ord("A") if char.isupper() else ord("a")
                encrypted_char = chr((ord(char) - base + self.shift) % 26 + base)
                ciphertext += encrypted_char
            else:
                ciphertext += char

        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ""

        for char in ciphertext:
            if char.isalpha():
                base = ord("A") if char.isupper() else ord("a")
                decrypted_char = chr((ord(char) - base - self.shift) % 26 + base)
                plaintext += decrypted_char
            else:
                plaintext += char

        return plaintext


def main():
    message = "Le Hoang Huy 2410060274"
    shift = 3

    cipher = CaesarCipher(shift)

    encrypted_message = cipher.encrypt(message)
    decrypted_message = cipher.decrypt(encrypted_message)

    print("=== CAESAR CIPHER ===")
    print("Plaintext:", message)
    print("Shift:", shift)
    print("Encrypted:", encrypted_message)
    print("Decrypted:", decrypted_message)


if __name__ == "__main__":
    main()