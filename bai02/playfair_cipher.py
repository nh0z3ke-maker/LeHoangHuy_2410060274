# 2.5.4 - Ma hoa va giai ma Playfair Cipher


class PlayfairCipher:
    def __init__(self, key):
        self.key = key
        self.matrix = self.create_matrix(key)

    def create_matrix(self, key):
        key = key.upper().replace("J", "I")
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        used_chars = []

        for char in key + alphabet:
            if char.isalpha() and char not in used_chars:
                used_chars.append(char)

        matrix = []
        for i in range(0, 25, 5):
            matrix.append(used_chars[i:i + 5])

        return matrix

    def display_matrix(self):
        print("=== PLAYFAIR MATRIX ===")
        for row in self.matrix:
            print(row)

    def find_position(self, char):
        char = char.upper().replace("J", "I")

        for row in range(5):
            for col in range(5):
                if self.matrix[row][col] == char:
                    return row, col

        return None

    def prepare_text(self, text):
        text = text.upper().replace("J", "I")
        text = "".join(char for char in text if char.isalpha())

        prepared_text = ""
        i = 0

        while i < len(text):
            char_1 = text[i]

            if i + 1 < len(text):
                char_2 = text[i + 1]

                if char_1 == char_2:
                    prepared_text += char_1 + "X"
                    i += 1
                else:
                    prepared_text += char_1 + char_2
                    i += 2
            else:
                prepared_text += char_1 + "X"
                i += 1

        return prepared_text

    def encrypt_pair(self, char_1, char_2):
        row_1, col_1 = self.find_position(char_1)
        row_2, col_2 = self.find_position(char_2)

        if row_1 == row_2:
            return (
                self.matrix[row_1][(col_1 + 1) % 5]
                + self.matrix[row_2][(col_2 + 1) % 5]
            )

        if col_1 == col_2:
            return (
                self.matrix[(row_1 + 1) % 5][col_1]
                + self.matrix[(row_2 + 1) % 5][col_2]
            )

        return self.matrix[row_1][col_2] + self.matrix[row_2][col_1]

    def decrypt_pair(self, char_1, char_2):
        row_1, col_1 = self.find_position(char_1)
        row_2, col_2 = self.find_position(char_2)

        if row_1 == row_2:
            return (
                self.matrix[row_1][(col_1 - 1) % 5]
                + self.matrix[row_2][(col_2 - 1) % 5]
            )

        if col_1 == col_2:
            return (
                self.matrix[(row_1 - 1) % 5][col_1]
                + self.matrix[(row_2 - 1) % 5][col_2]
            )

        return self.matrix[row_1][col_2] + self.matrix[row_2][col_1]

    def encrypt(self, plaintext):
        plaintext = self.prepare_text(plaintext)
        ciphertext = ""

        for i in range(0, len(plaintext), 2):
            ciphertext += self.encrypt_pair(plaintext[i], plaintext[i + 1])

        return ciphertext

    def decrypt(self, ciphertext):
        ciphertext = ciphertext.upper()
        plaintext = ""

        for i in range(0, len(ciphertext), 2):
            plaintext += self.decrypt_pair(ciphertext[i], ciphertext[i + 1])

        return plaintext


def main():
    key = "SECURITY"
    message = "LEHOANGHUY"

    cipher = PlayfairCipher(key)

    encrypted_message = cipher.encrypt(message)
    decrypted_message = cipher.decrypt(encrypted_message)

    cipher.display_matrix()

    print("\n=== PLAYFAIR CIPHER ===")
    print("Plaintext:", message)
    print("Key:", key)
    print("Encrypted:", encrypted_message)
    print("Decrypted:", decrypted_message)


if __name__ == "__main__":
    main()