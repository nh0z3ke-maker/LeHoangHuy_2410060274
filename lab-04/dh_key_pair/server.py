# Bai 4.6.2 - Le Hoang Huy - 2410060274 - 24TXTHG1
# Tao cap khoa Diffie-Hellman va luu khoa cong khai cua server.

from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dh


BASE_DIR = Path(__file__).resolve().parent
PUBLIC_KEY_FILE = BASE_DIR / "server_public_key.pem"


def main():
    print("BAI 4.6.2 - TAO CAP KHOA DIFFIE-HELLMAN", flush=True)
    print("LE HOANG HUY | 2410060274 | 24TXTHG1", flush=True)
    print("Dang tao tham so DH 2048 bit, g = 2. Vui long cho...", flush=True)

    # Tao bo tham so dung cho Diffie-Hellman.
    parameters = dh.generate_parameters(generator=2, key_size=2048)

    # Tao khoa bi mat va lay khoa cong khai tuong ung.
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()

    # Chuyen khoa cong khai sang dinh dang PEM.
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # Luu tep cung thu muc voi server.py de client doc o buoc sau.
    PUBLIC_KEY_FILE.write_bytes(public_pem)

    print(f"[OK] Da tao cap khoa DH {private_key.key_size} bit.", flush=True)
    print(f"[OK] Da luu khoa cong khai: {PUBLIC_KEY_FILE.name}", flush=True)
    print("\nKhoa cong khai cua server (PEM):", flush=True)
    print(public_pem.decode("ascii"), flush=True)
    print("Hoan thanh. Tiep theo: chay client.py.", flush=True)


if __name__ == "__main__":
    main()