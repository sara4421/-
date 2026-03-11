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
    print("\nPlease select the operation you wish to perform:")
    print("To add a student, press a")
    print("To delete a student, press d")
    print("To update student information, press u")
    print("To view student information, press s")


def main():
    while True:
        menu()
        choice = input("Your choice: ").lower()

        if choice == 'a':

            student_id_input = input("Enter student ID: ")
            if not student_id_input.isdigit():
                print("Error: Student ID must be a number.")
                continue
            student_id = int(student_id_input)

            first_name = input("Enter first name: ")
            if not first_name.isalpha():
                print("Error: First name must contain letters only.")
                continue

            last_name = input("Enter last name: ")
            if not last_name.isalpha():
                print("Error: Last name must contain letters only.")
                continue

            age_input = input("Enter age: ")
            if not age_input.isdigit():
                print("Error: Age must be a number.")
                continue
            age = int(age_input)

            grade = input("Enter grade: ")
            registration_date = input("Enter registration date (YYYY-MM-DD): ")

            lessons_input = input("Enter lesson names separated by comma: ")
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

            print(f"Student {first_name} added successfully.")

        elif choice == 'd':

            student_id_input = input("Enter student ID to delete: ")
            if not student_id_input.isdigit():
                print("Error: Student ID must be a number.")
                continue
            student_id = int(student_id_input)

            conn = sqlite3.connect("school.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            student = cursor.fetchone()

            if student:
                cursor.execute("DELETE FROM student_lessons WHERE student_id = ?", (student_id,))
                cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
                conn.commit()
                print("Student deleted successfully.")
            else:
                print("Student ID not found.")

            conn.close()

        elif choice == 'u':

            student_id_input = input("Enter student ID to update: ")
            if not student_id_input.isdigit():
                print("Error: Student ID must be a number.")
                continue
            student_id = int(student_id_input)

            conn = sqlite3.connect("school.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            student = cursor.fetchone()

            if student:

                first_name = input(f"Enter first name [{student[1]}]: ") or student[1]
                if not first_name.isalpha():
                    print("Error: First name must contain letters only.")
                    conn.close()
                    continue

                last_name = input(f"Enter last name [{student[2]}]: ") or student[2]
                if not last_name.isalpha():
                    print("Error: Last name must contain letters only.")
                    conn.close()
                    continue

                age_input = input(f"Enter age [{student[3]}]: ") or str(student[3])
                if not age_input.isdigit():
                    print("Error: Age must be a number.")
                    conn.close()
                    continue
                age = int(age_input)

                grade = input(f"Enter grade [{student[4]}]: ") or student[4]
                registration_date = input(f"Enter registration date [{student[5]}]: ") or student[5]

                cursor.execute("""
                    UPDATE students
                    SET first_name=?, last_name=?, age=?, grade=?, registration_date=?
                    WHERE student_id=?
                """, (first_name, last_name, age, grade, registration_date, student_id))

                lessons_input = input("Enter lesson names separated by comma (leave empty if unchanged): ")

                if lessons_input.strip():
                    lessons_list = [lesson.strip() for lesson in lessons_input.split(",")]

                    cursor.execute("DELETE FROM student_lessons WHERE student_id = ?", (student_id,))

                    for lesson_name in lessons_list:
                        cursor.execute("INSERT OR IGNORE INTO lessons (lesson_name) VALUES (?)", (lesson_name,))
                        cursor.execute("SELECT lesson_id FROM lessons WHERE lesson_name = ?", (lesson_name,))
                        lesson_id = cursor.fetchone()[0]

                        cursor.execute("INSERT INTO student_lessons VALUES (?, ?)", (student_id, lesson_id))

                conn.commit()

                print("Student information updated successfully.")

            else:
                print("Student ID not found.")

            conn.close()

        elif choice == 's':

            student_id_input = input("Enter student ID to view: ")
            if not student_id_input.isdigit():
                print("Error: Student ID must be a number.")
                continue
            student_id = int(student_id_input)

            conn = sqlite3.connect("school.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            student = cursor.fetchone()

            if student:

                print("\nStudent Information:")
                print("Student ID:", student[0])
                print("First Name:", student[1])
                print("Last Name:", student[2])
                print("Age:", student[3])
                print("Grade:", student[4])
                print("Registration Date:", student[5])

                cursor.execute("""
                SELECT lesson_name
                FROM lessons
                JOIN student_lessons ON lessons.lesson_id = student_lessons.lesson_id
                WHERE student_lessons.student_id = ?
                """, (student_id,))

                lessons = cursor.fetchall()
                lessons_names = [l[0] for l in lessons]

                print("Lessons:", ", ".join(lessons_names))

            else:
                print("Student ID not found.")

            conn.close()

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()