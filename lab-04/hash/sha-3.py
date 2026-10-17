# Bai 4.6.3 - Le Hoang Huy - 2410060274 - 24TXTHG1
# Bam SHA3-256 bang thu vien PyCryptodome.

from Crypto.Hash import SHA3_256


def sha3_256_hash(text):
    data = text.encode("utf-8")
    return SHA3_256.new(data=data).hexdigest()


def main():
    print("BAI 4.6.3 - HAM BAM SHA3-256")
    print("LE HOANG HUY | 2410060274 | 24TXTHG1")

    text = input("Nhap chuoi can bam: ")
    digest = sha3_256_hash(text)

    print(f"\nChuoi dau vao: {text}")
    print(f"SHA3-256: {digest}")
    print(f"Do dai: {len(digest)} ky tu hex (256 bit)")


if __name__ == "__main__":
    main()