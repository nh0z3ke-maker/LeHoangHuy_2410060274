# 1.6.2 - Lap trinh Python co ban

print("=== THONG TIN SINH VIEN ===")
ho_ten = "Le Hoang Huy"
mssv = "2410060274"
lop = "ECOS339"

print("Ho ten:", ho_ten)
print("MSSV:", mssv)
print("Lop:", lop)

print("\n=== KIEU DU LIEU CO BAN ===")
so_nguyen = 10
so_thuc = 8.5
chuoi = "Bao mat thong tin nang cao"
dung_sai = True

print("So nguyen:", so_nguyen, type(so_nguyen))
print("So thuc:", so_thuc, type(so_thuc))
print("Chuoi:", chuoi, type(chuoi))
print("Dung sai:", dung_sai, type(dung_sai))

print("\n=== PHEP TOAN ===")
a = 15
b = 4

print("a =", a)
print("b =", b)
print("Tong:", a + b)
print("Hieu:", a - b)
print("Tich:", a * b)
print("Thuong:", a / b)
print("Chia lay nguyen:", a // b)
print("Chia lay du:", a % b)
print("Luy thua:", a ** b)

print("\n=== CAU TRUC DIEU KIEN ===")
diem = 8.0

if diem >= 8:
    print("Xep loai: Gioi")
elif diem >= 6.5:
    print("Xep loai: Kha")
elif diem >= 5:
    print("Xep loai: Trung binh")
else:
    print("Xep loai: Yeu")

print("\n=== VONG LAP FOR ===")
for i in range(1, 6):
    print("Lan lap thu", i)

print("\n=== VONG LAP WHILE ===")
dem = 1
while dem <= 5:
    print("Gia tri dem:", dem)
    dem += 1

print("\n=== HAM TRONG PYTHON ===")


def tinh_tong(x, y):
    return x + y


def kiem_tra_chan_le(n):
    if n % 2 == 0:
        return "So chan"
    return "So le"


print("Tong 7 + 9 =", tinh_tong(7, 9))
print("Kiem tra so 10:", kiem_tra_chan_le(10))
print("Kiem tra so 15:", kiem_tra_chan_le(15))