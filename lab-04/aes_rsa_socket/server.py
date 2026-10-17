# Bai 4.6.1 - Le Hoang Huy - 2410060274 - 24TXTHG1

import socket
import struct
import threading

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


HOST = "127.0.0.1"
PORT = 12345
MAX_PACKET_SIZE = 65536

clients = {}
clients_lock = threading.Lock()


def send_packet(connection, data):
    if not 0 < len(data) <= MAX_PACKET_SIZE:
        raise ValueError("Kich thuoc goi du lieu khong hop le.")

    header = struct.pack("!I", len(data))
    connection.sendall(header + data)


def recv_exact(connection, size):
    data = bytearray()

    while len(data) < size:
        chunk = connection.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Client da ngat ket noi.")

        data.extend(chunk)

    return bytes(data)


def recv_packet(connection):
    header = recv_exact(connection, 4)
    size = struct.unpack("!I", header)[0]

    if not 0 < size <= MAX_PACKET_SIZE:
        raise ValueError("Kich thuoc goi du lieu khong hop le.")

    return recv_exact(connection, size)


def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    data = pad(message.encode("utf-8"), AES.block_size)

    return cipher.iv + cipher.encrypt(data)


def decrypt_message(key, encrypted_message):
    if (
        len(encrypted_message) < 2 * AES.block_size
        or len(encrypted_message) % AES.block_size != 0
    ):
        raise ValueError("Ban ma AES khong hop le.")

    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return plaintext.decode("utf-8")


def broadcast_message(sender, message):
    with clients_lock:
        recipients = list(clients.items())

    for connection, (key, send_lock) in recipients:
        if connection is sender:
            continue

        try:
            encrypted_message = encrypt_message(key, message)

            with send_lock:
                send_packet(connection, encrypted_message)

        except OSError as error:
            print(f"[GUI LOI] {error}", flush=True)


def handle_client(connection, address, server_key):
    label = f"{address[0]}:{address[1]}"
    print(f"[KET NOI] {label}", flush=True)

    try:
        # Gui khoa cong khai RSA cua server.
        server_public_key = server_key.publickey().export_key()
        send_packet(connection, server_public_key)

        # Nhan khoa cong khai RSA cua client.
        client_public_key = RSA.import_key(recv_packet(connection))

        # Tao khoa AES-128 rieng cho client nay.
        aes_key = get_random_bytes(16)

        # Ma hoa khoa AES bang khoa cong khai RSA cua client.
        cipher_rsa = PKCS1_OAEP.new(client_public_key)
        encrypted_key = cipher_rsa.encrypt(aes_key)

        send_lock = threading.Lock()

        with send_lock:
            with clients_lock:
                clients[connection] = (aes_key, send_lock)

            send_packet(connection, encrypted_key)

        print(
            f"[SAN SANG] {label} | Da trao doi khoa AES bang RSA.",
            flush=True,
        )

        while True:
            encrypted_message = recv_packet(connection)
            message = decrypt_message(aes_key, encrypted_message)

            print(f"[NHAN] {label}: {message}", flush=True)

            if message == "exit":
                break

            # Ma hoa lai tin nhan bang khoa AES cua tung client nhan.
            broadcast_message(connection, message)

    except (OSError, ValueError) as error:
        print(f"[DONG KET NOI] {label}: {error}", flush=True)

    finally:
        with clients_lock:
            clients.pop(connection, None)

        connection.close()
        print(f"[DA DONG] {label}", flush=True)


def main():
    print("BAI 4.6.1 - SOCKET VOI AES VA RSA", flush=True)
    print("LE HOANG HUY | 2410060274 | 24TXTHG1", flush=True)
    print("Dang tao cap khoa RSA 2048 bit...", flush=True)

    server_key = RSA.generate(2048)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)

        # Cho toi da 1 giay moi lan accept de xu ly Ctrl+C.
        server.settimeout(1.0)

        print(f"Server dang lang nghe tai {HOST}:{PORT}", flush=True)
        print(
            "Ma hoa tin nhan: AES-128-CBC | Trao doi khoa: RSA-OAEP",
            flush=True,
        )

        try:
            while True:
                try:
                    connection, address = server.accept()

                except socket.timeout:
                    continue

                threading.Thread(
                    target=handle_client,
                    args=(connection, address, server_key),
                    daemon=True,
                ).start()

        except KeyboardInterrupt:
            print("\nServer da dung.", flush=True)


if __name__ == "__main__":
    main()