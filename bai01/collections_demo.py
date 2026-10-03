# 1.6.3 - List, Tuple, Dictionary trong Python

print("=== LIST ===")
mon_hoc = ["Python", "Git", "Flask", "Cryptography"]

print("Danh sach mon hoc:", mon_hoc)
print("Mon hoc dau tien:", mon_hoc[0])
print("Mon hoc cuoi cung:", mon_hoc[-1])

mon_hoc.append("Security")
print("Sau khi them Security:", mon_hoc)

mon_hoc.remove("Git")
print("Sau khi xoa Git:", mon_hoc)

print("Duyet danh sach mon hoc:")
for mon in mon_hoc:
    print("-", mon)

print("\n=== TUPLE ===")
thong_tin = ("Le Hoang Huy", "2410060274", "ECOS339")

print("Tuple thong tin:", thong_tin)
print("Ho ten:", thong_tin[0])
print("MSSV:", thong_tin[1])
print("Lop:", thong_tin[2])

print("\n=== DICTIONARY ===")
sinh_vien = {
    "ho_ten": "Le Hoang Huy",
    "mssv": "2410060274",
    "lop": "ECOS339",
    "diem": 8.5,
}

print("Thong tin sinh vien:", sinh_vien)
print("Ho ten:", sinh_vien["ho_ten"])
print("MSSV:", sinh_vien["mssv"])
print("Diem:", sinh_vien["diem"])

sinh_vien["xep_loai"] = "Gioi"
print("Sau khi them xep loai:", sinh_vien)

print("\nDuyet dictionary:")
for key, value in sinh_vien.items():
    print(key, ":", value)

print("\n=== DANH SACH DICTIONARY ===")
danh_sach_sinh_vien = [
    {"ho_ten": "Le Hoang Huy", "mssv": "2410060274", "diem": 8.5},
    {"ho_ten": "Nguyen Van A", "mssv": "2410060001", "diem": 7.0},
    {"ho_ten": "Tran Thi B", "mssv": "2410060002", "diem": 9.0},
]

for sv in danh_sach_sinh_vien:
    print(sv["ho_ten"], "-", sv["mssv"], "-", sv["diem"])