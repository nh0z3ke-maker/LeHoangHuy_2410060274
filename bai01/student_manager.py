# 1.6.4 - OOP trong Python


class Student:
    def __init__(self, student_id, full_name, age, major, score):
        self.student_id = student_id
        self.full_name = full_name
        self.age = age
        self.major = major
        self.score = score

    def get_rank(self):
        if self.score >= 8:
            return "Gioi"
        if self.score >= 6.5:
            return "Kha"
        if self.score >= 5:
            return "Trung binh"
        return "Yeu"

    def display_info(self):
        print("Ma sinh vien:", self.student_id)
        print("Ho ten:", self.full_name)
        print("Tuoi:", self.age)
        print("Nganh:", self.major)
        print("Diem:", self.score)
        print("Xep loai:", self.get_rank())
        print("-" * 30)


class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def show_students(self):
        if len(self.students) == 0:
            print("Danh sach sinh vien dang rong.")
            return

        print("=== DANH SACH SINH VIEN ===")
        for student in self.students:
            student.display_info()

    def find_student_by_id(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def update_score(self, student_id, new_score):
        student = self.find_student_by_id(student_id)

        if student is None:
            print("Khong tim thay sinh vien co ma:", student_id)
            return

        student.score = new_score
        print("Da cap nhat diem cho sinh vien:", student.full_name)

    def delete_student(self, student_id):
        student = self.find_student_by_id(student_id)

        if student is None:
            print("Khong tim thay sinh vien co ma:", student_id)
            return

        self.students.remove(student)
        print("Da xoa sinh vien:", student.full_name)


def main():
    manager = StudentManager()

    student_1 = Student(
        "2410060274",
        "Le Hoang Huy",
        22,
        "Bao mat thong tin",
        8.5,
    )

    student_2 = Student(
        "2410060001",
        "Nguyen Van A",
        21,
        "Cong nghe thong tin",
        7.0,
    )

    student_3 = Student(
        "2410060002",
        "Tran Thi B",
        20,
        "An toan thong tin",
        9.0,
    )

    manager.add_student(student_1)
    manager.add_student(student_2)
    manager.add_student(student_3)

    manager.show_students()

    print("=== TIM SINH VIEN ===")
    found_student = manager.find_student_by_id("2410060274")
    if found_student is not None:
        found_student.display_info()
    else:
        print("Khong tim thay sinh vien.")

    print("=== CAP NHAT DIEM ===")
    manager.update_score("2410060274", 9.2)
    manager.show_students()

    print("=== XOA SINH VIEN ===")
    manager.delete_student("2410060001")
    manager.show_students()


if __name__ == "__main__":
    main()