# Bai 4.6.3 - Le Hoang Huy - 2410060274 - 24TXTHG1
# Tu cai dat MD5 theo mo ta thuat toan trong RFC 1321.

import math
import struct


MASK32 = 0xFFFFFFFF

# So bit xoay trai cua 64 buoc, chia thanh 4 vong.
SHIFTS = (
    [7, 12, 17, 22] * 4
    + [5, 9, 14, 20] * 4
    + [4, 11, 16, 23] * 4
    + [6, 10, 15, 21] * 4
)

# Bang 64 hang so cua MD5, tinh tu ham sin (don vi radian).
CONSTANTS = [
    int(abs(math.sin(index + 1)) * (1 << 32)) & MASK32
    for index in range(64)
]


def left_rotate(value, shift):
    """Xoay trai mot gia tri trong pham vi 32 bit."""
    value &= MASK32
    return ((value << shift) | (value >> (32 - shift))) & MASK32


def md5_hash(text):
    """Tra ve chuoi MD5 gom 32 ky tu hex cua van ban UTF-8."""
    data = bytearray(text.encode("utf-8"))
    original_bit_length = (len(data) * 8) & 0xFFFFFFFFFFFFFFFF

    # Them bit 1, sau do them cac bit 0 de do dai dat 56 modulo 64 byte.
    data.append(0x80)
    while len(data) % 64 != 56:
        data.append(0)

    # Ghep do dai ban dau theo bit, gom 8 byte little-endian.
    data.extend(struct.pack("<Q", original_bit_length))

    # Khoi tao bon thanh ghi 32 bit.
    a0 = 0x67452301
    b0 = 0xEFCDAB89
    c0 = 0x98BADCFE
    d0 = 0x10325476

    # Moi khoi 64 byte duoc chia thanh 16 tu 32 bit little-endian.
    for offset in range(0, len(data), 64):
        words = struct.unpack("<16I", data[offset:offset + 64])
        a, b, c, d = a0, b0, c0, d0

        for index in range(64):
            if index < 16:
                f = (b & c) | ((~b) & d)
                g = index
            elif index < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * index + 1) % 16
            elif index < 48:
                f = b ^ c ^ d
                g = (3 * index + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * index) % 16

            value = (a + f + CONSTANTS[index] + words[g]) & MASK32
            new_b = (b + left_rotate(value, SHIFTS[index])) & MASK32
            a, b, c, d = d, new_b, b, c

        # Cong ket qua khoi hien tai vao trang thai tich luy.
        a0 = (a0 + a) & MASK32
        b0 = (b0 + b) & MASK32
        c0 = (c0 + c) & MASK32
        d0 = (d0 + d) & MASK32

    # Ghep bon thanh ghi thanh 16 byte, sau do doi sang hex.
    return struct.pack("<4I", a0, b0, c0, d0).hex()


def main():
    print("BAI 4.6.3 - TU CAI DAT THUAT TOAN MD5")
    print("LE HOANG HUY | 2410060274 | 24TXTHG1")

    text = input("Nhap chuoi can bam: ")
    digest = md5_hash(text)

    print(f"\nChuoi dau vao: {text}")
    print(f"MD5 (tu cai dat): {digest}")
    print(f"Do dai: {len(digest)} ky tu hex (128 bit)")


if __name__ == "__main__":
    main()