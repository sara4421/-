import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    age INTEGER,
    grade TEXT,
    registration_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS lessons (
    lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_name TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS student_lessons (
    student_id INTEGER,
    lesson_id INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(student_id),
    FOREIGN KEY(lesson_id) REFERENCES lessons(lesson_id)
)
""")

conn.commit()
conn.close()


def menu():
    print("\nالرجاء اختيار العملية التي تريد إجرائها:")
    print("لإضافة طالب اضغط a")
    print("لحذف طالب اضغط d")
    print("لتعديل معلومات طالب اضغط u")
    print("لعرض معلومات طالب اضغط s")


def main():
    while True:
        menu()
        choice = input("اختيارك: ").lower()

        if choice == 'a':
            student_id = int(input("أدخل رقم الطالب: "))
            first_name = input("أدخل الاسم الأول: ")
            last_name = input("أدخل الكنية: ")
            age = int(input("أدخل العمر: "))
            grade = input("أدخل الصف: ")
            registration_date = input("أدخل تاريخ التسجيل (YYYY-MM-DD): ")

            lessons_input = input("أدخل أسماء الدروس مفصولة بفاصلة: ")
            lessons_list = [lesson.strip() for lesson in lessons_input.split(",")]

            conn = sqlite3.connect("school.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)",
                           (student_id, first_name, last_name, age, grade, registration_date))

            for lesson_name in lessons_list:
                cursor.execute("INSERT OR IGNORE INTO lessons (lesson_name) VALUES (?)", (lesson_name,))
                cursor.execute("SELECT lesson_id FROM lessons WHERE lesson_name = ?", (lesson_name,))
                lesson_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO student_lessons (student_id, lesson_id) VALUES (?, ?)",
                               (student_id, lesson_id))

            conn.commit()
            conn.close()
            print(f"تمت إضافة الطالب {first_name} بنجاح ")

        elif choice == 'd':
            student_id = int(input("أدخل رقم الطالب الذي تريد حذفه: "))
            conn = sqlite3.connect("school.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            student = cursor.fetchone()

            if student:
                cursor.execute("DELETE FROM student_lessons WHERE student_id = ?", (student_id,))
                cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
                conn.commit()
                print(f"تم حذف الطالب رقم {student_id} بنجاح ")
            else:
                print("رقم الطالب غير موجود ")

            conn.close()

        elif choice == 'u':
            student_id = int(input("أدخل رقم الطالب الذي تريد تعديل معلوماته: "))
            conn = sqlite3.connect("school.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            student = cursor.fetchone()

            if student:
                first_name = input(f"أدخل الاسم الأول [{student[1]}]: ") or student[1]
                last_name = input(f"أدخل الكنية [{student[2]}]: ") or student[2]
                age = input(f"أدخل العمر [{student[3]}]: ") or student[3]
                grade = input(f"أدخل الصف [{student[4]}]: ") or student[4]
                registration_date = input(f"أدخل تاريخ التسجيل [{student[5]}]: ") or student[5]

                cursor.execute("""
                    UPDATE students SET first_name=?, last_name=?, age=?, grade=?, registration_date=? 
                    WHERE student_id=?
                """, (first_name, last_name, age, grade, registration_date, student_id))

                lessons_input = input("أدخل أسماء الدروس مفصولة بفاصلة (اتركها فارغة إذا لم تتغير): ")
                if lessons_input.strip():
                    lessons_list = [lesson.strip() for lesson in lessons_input.split(",")]
                    cursor.execute("DELETE FROM student_lessons WHERE student_id = ?", (student_id,))
                    for lesson_name in lessons_list:
                        cursor.execute("INSERT OR IGNORE INTO lessons (lesson_name) VALUES (?)", (lesson_name,))
                        cursor.execute("SELECT lesson_id FROM lessons WHERE lesson_name = ?", (lesson_name,))
                        lesson_id = cursor.fetchone()[0]
                        cursor.execute("INSERT INTO student_lessons (student_id, lesson_id) VALUES (?, ?)",
                                       (student_id, lesson_id))

                conn.commit()
                print(f"تم تعديل بيانات الطالب {first_name} بنجاح ")
            else:
                print("رقم الطالب غير موجود ")

            conn.close()

        elif choice == 's':
            student_id = int(input("أدخل رقم الطالب الذي تريد عرض معلوماته: "))
            conn = sqlite3.connect("school.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            student = cursor.fetchone()

            if student:
                print(f"\nمعلومات الطالب:")
                print(f"رقم الطالب: {student[0]}")
                print(f"الاسم: {student[1]}")
                print(f"الكنية: {student[2]}")
                print(f"العمر: {student[3]}")
                print(f"الصف: {student[4]}")
                print(f"تاريخ التسجيل: {student[5]}")

                cursor.execute("""
                    SELECT lesson_name FROM lessons 
                    JOIN student_lessons ON lessons.lesson_id = student_lessons.lesson_id
                    WHERE student_lessons.student_id = ?
                """, (student_id,))
                lessons = cursor.fetchall()
                lessons_names = [l[0] for l in lessons]
                print(f"الدروس المسجلة فيها: {', '.join(lessons_names)}")
            else:
                print("رقم الطالب غير موجود ")

            conn.close()

        else:
            print("اختيار غير صحيح، حاول مرة أخرى.")


if __name__ == "__main__":
    main()