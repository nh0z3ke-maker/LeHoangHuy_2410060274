# Bai 4.6.3 - Le Hoang Huy - 2410060274 - 24TXTHG1
# Bam BLAKE2b voi ket qua 64 byte (512 bit).

import hashlib


def blake2b_hash(text):
    data = text.encode("utf-8")
    return hashlib.blake2b(data, digest_size=64).hexdigest()


def main():
    print("BAI 4.6.3 - HAM BAM BLAKE2b-512")
    print("LE HOANG HUY | 2410060274 | 24TXTHG1")

    text = input("Nhap chuoi can bam: ")
    digest = blake2b_hash(text)

    print(f"\nChuoi dau vao: {text}")
    print(f"BLAKE2b-512: {digest}")
    print(f"Do dai: {len(digest)} ky tu hex (512 bit)")


if __name__ == "__main__":
    main()
    