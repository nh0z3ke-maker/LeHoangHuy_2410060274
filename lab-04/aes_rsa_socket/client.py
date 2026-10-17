# Bai 4.6.1 - Le Hoang Huy - 2410060274 - 24TXTHG1
import socket
import struct
import threading

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad

HOST = "127.0.0.1"
PORT = 12345
MAX_PACKET_SIZE = 65536


def send_packet(connection, data):
    if not 0 < len(data) <= MAX_PACKET_SIZE:
        raise ValueError("Kich thuoc goi du lieu khong hop le.")
    connection.sendall(struct.pack("!I", len(data)) + data)


def recv_exact(connection, size):
    data = bytearray()
    while len(data) < size:
        chunk = connection.recv(size - len(data))
        if not chunk:
            raise ConnectionError("Server da ngat ket noi.")
        data.extend(chunk)
    return bytes(data)


def recv_packet(connection):
    size = struct.unpack("!I", recv_exact(connection, 4))[0]
    if not 0 < size <= MAX_PACKET_SIZE:
        raise ValueError("Kich thuoc goi du lieu khong hop le.")
    return recv_exact(connection, size)


def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    data = pad(message.encode("utf-8"), AES.block_size)
    return cipher.iv + cipher.encrypt(data)


def decrypt_message(key, encrypted_message):
    if len(encrypted_message) < 32 or len(encrypted_message) % 16:
        raise ValueError("Ban ma AES khong hop le.")
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode("utf-8")


def receive_messages(connection, aes_key, stopped):
    try:
        while not stopped.is_set():
            encrypted_message = recv_packet(connection)
            message = decrypt_message(aes_key, encrypted_message)
            print(f"\n[NHAN] {message}\nBan: ", end="", flush=True)
    except (OSError, ValueError) as error:
        if not stopped.is_set():
            print(f"\n[MAT KET NOI] {error}", flush=True)
            print("Nhan Enter de ket thuc client.", flush=True)
    finally:
        stopped.set()


def main():
    print("CLIENT - SOCKET VOI AES VA RSA", flush=True)
    print("LE HOANG HUY | 2410060274 | 24TXTHG1", flush=True)
    print("Dang tao cap khoa RSA 2048 bit...", flush=True)
    client_key = RSA.generate(2048)
    stopped = threading.Event()
    receiver = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        try:
            connection.settimeout(10)
            connection.connect((HOST, PORT))

            server_public_key = RSA.import_key(recv_packet(connection))
            print(
                f"[SERVER] Da nhan khoa RSA {server_public_key.size_in_bits()} bit.",
                flush=True,
            )
            send_packet(connection, client_key.publickey().export_key())

            encrypted_key = recv_packet(connection)
            aes_key = PKCS1_OAEP.new(client_key).decrypt(encrypted_key)
            if len(aes_key) != 16:
                raise ValueError("Khoa AES nhan duoc khong hop le.")
            connection.settimeout(None)

            print("[SAN SANG] Da nhan va giai ma khoa AES-128.", flush=True)
            print("Nhap tin nhan de gui. Go exit de thoat.", flush=True)

            receiver = threading.Thread(
                target=receive_messages,
                args=(connection, aes_key, stopped),
                daemon=True,
            )
            receiver.start()

            while not stopped.is_set():
                message = input("Ban: ")
                if stopped.is_set():
                    break
                if not message.strip():
                    continue

                encrypted_message = encrypt_message(aes_key, message)
                if len(encrypted_message) > MAX_PACKET_SIZE:
                    print("Tin nhan qua dai. Hay nhap ngan hon.", flush=True)
                    continue

                if message == "exit":
                    stopped.set()
                send_packet(connection, encrypted_message)

        except ConnectionRefusedError:
            print(
                "[LOI] Chua ket noi duoc server. Hay chay server.py truoc.",
                flush=True,
            )
        except (KeyboardInterrupt, EOFError):
            print("\nDang ngat ket noi...", flush=True)
        except (OSError, ValueError) as error:
            print(f"[LOI] {error}", flush=True)
        finally:
            stopped.set()
            try:
                connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            if receiver is not None:
                receiver.join(timeout=1)

    print("Client da dong.", flush=True)


if __name__ == "__main__":
    main()