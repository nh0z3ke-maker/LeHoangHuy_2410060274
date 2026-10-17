# Bai 4.6.3 - Le Hoang Huy - 2410060274 - 24TXTHG1
# Bam MD5 bang thu vien hashlib cua Python.

import hashlib


def md5_hash(text):
    data = text.encode("utf-8")
    return hashlib.md5(data).hexdigest()


def main():
    print("BAI 4.6.3 - MD5 BANG THU VIEN HASHLIB")
    print("LE HOANG HUY | 2410060274 | 24TXTHG1")

    text = input("Nhap chuoi can bam: ")
    digest = md5_hash(text)

    print(f"\nChuoi dau vao: {text}")
    print(f"MD5 (hashlib): {digest}")
    print(f"Do dai: {len(digest)} ky tu hex (128 bit)")


if __name__ == "__main__":
    main()