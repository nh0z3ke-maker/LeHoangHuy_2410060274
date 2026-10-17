# Bai 4.6.2 - Le Hoang Huy - 2410060274 - 24TXTHG1
# Doc khoa cong khai cua server va tinh bi mat chung Diffie-Hellman.

from pathlib import Path

from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dh


BASE_DIR = Path(__file__).resolve().parent
PUBLIC_KEY_FILE = BASE_DIR / "server_public_key.pem"


def main():
    print("BAI 4.6.2 - CLIENT DIFFIE-HELLMAN", flush=True)
    print("LE HOANG HUY | 2410060274 | 24TXTHG1", flush=True)

    # Doc va khoi phuc khoa cong khai cua server tu tep PEM.
    public_pem = PUBLIC_KEY_FILE.read_bytes()
    server_public_key = serialization.load_pem_public_key(public_pem)

    if not isinstance(server_public_key, dh.DHPublicKey):
        raise ValueError("Tep PEM khong chua khoa cong khai Diffie-Hellman.")

    print(f"[OK] Da doc {PUBLIC_KEY_FILE.name}.", flush=True)

    # Client dung cung bo tham so DH voi server.
    parameters = server_public_key.parameters()
    client_private_key = parameters.generate_private_key()
    client_public_key = client_private_key.public_key()

    print(
        f"[OK] Da tao cap khoa DH {client_public_key.key_size} bit cua client.",
        flush=True,
    )

    # Ket hop khoa bi mat cua client voi khoa cong khai cua server.
    shared_secret = client_private_key.exchange(server_public_key)

    print("[OK] Da tinh bi mat chung (Shared Secret).", flush=True)
    print(f"Do dai Shared Secret: {len(shared_secret)} byte", flush=True)
    print("\nShared Secret (hex):", flush=True)

    # Chia chuoi hex thanh tung dong de de quan sat va chup bao cao.
    secret_hex = shared_secret.hex()
    for start in range(0, len(secret_hex), 64):
        print(secret_hex[start:start + 64], flush=True)

    print("\nHoan thanh.", flush=True)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        print("[LOI] Chua co server_public_key.pem. Hay chay server.py truoc.")
        raise SystemExit(1)
    except (OSError, ValueError, UnsupportedAlgorithm) as error:
        print(f"[LOI] {error}")
        raise SystemExit(1)