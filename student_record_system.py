"""Student Record and Academic Management System.

Run with Python 3. Student records are saved in student_records.json beside
this program so they are available the next time it is opened.
"""

import json
from pathlib import Path


DATA_FILE = Path(__file__).with_name("student_records.json")


def load_students():
    """Load saved records, returning an empty list if none exist yet."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            students = json.load(file)
        return students if isinstance(students, list) else []
    except (json.JSONDecodeError, OSError):
        print("Could not read the saved records. Starting with an empty list.")
        return []


def save_students(students):
    """Save records as readable JSON."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(students, file, indent=4, ensure_ascii=False)


def prompt_text(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("This field cannot be empty.")


def prompt_marks():
    """Collect marks for any number of subjects; each mark is out of 100."""
    while True:
        try:
            count = int(input("How many subjects? ").strip())
            if count > 0:
                break
            print("Enter at least one subject.")
        except ValueError:
            print("Enter a whole number.")

    marks = {}
    for number in range(1, count + 1):
        subject = prompt_text(f"Subject {number} name: ")
        while subject in marks:
            print("That subject has already been entered. Use a different name.")
            subject = prompt_text(f"Subject {number} name: ")

        while True:
            try:
                mark = float(input(f"Marks for {subject} (0-100): ").strip())
                if 0 <= mark <= 100:
                    marks[subject] = mark
                    break
                print("Marks must be between 0 and 100.")
            except ValueError:
                print("Enter a valid number.")
    return marks


def calculate_result(marks):
    total = sum(marks.values())
    average = total / len(marks) if marks else 0
    if average >= 80:
        grade = "A"
    elif average >= 70:
        grade = "B"
    elif average >= 60:
        grade = "C"
    else:
        grade = "F"
    return total, average, grade


def find_student(students, search_value):
    search_value = search_value.strip().casefold()
    for student in students:
        if (student["roll_number"].casefold() == search_value
                or student["prn"].casefold() == search_value):
            return student
    return None


def display_student(student):
    total, average, grade = calculate_result(student["marks"])
    print("\n" + "-" * 42)
    print("STUDENT ACADEMIC RECORD")
    print("-" * 42)
    print(f"Roll Number : {student['roll_number']}")
    print(f"Name        : {student['name']}")
    print(f"PRN         : {student['prn']}")
    print(f"Class       : {student['class_name']}")
    print(f"Division    : {student['division']}")
    print("Subject Marks:")
    for subject, mark in student["marks"].items():
        print(f"  {subject}: {mark:g}/100")
    print(f"Total Marks : {total:g}")
    print(f"Average     : {average:.2f}")
    print(f"Grade       : {grade}")
    print("-" * 42)


def add_student(students):
    print("\nADD STUDENT")
    roll_number = prompt_text("Roll number: ")
    prn = prompt_text("PRN: ")
    if any(s["roll_number"].casefold() == roll_number.casefold()
           or s["prn"].casefold() == prn.casefold() for s in students):
        print("A student with this roll number or PRN already exists.")
        return

    student = {
        "roll_number": roll_number,
        "name": prompt_text("Name: "),
        "prn": prn,
        "class_name": prompt_text("Class: "),
        "division": prompt_text("Division: "),
        "marks": prompt_marks(),
    }
    students.append(student)
    save_students(students)
    print("Student Added Successfully.")


def search_student(students):
    key = input("Enter roll number or PRN: ").strip()
    student = find_student(students, key)
    if student:
        display_student(student)
    else:
        print("Student Not Found.")


def update_student(students):
    key = input("Enter the student's roll number or PRN to update: ").strip()
    student = find_student(students, key)
    if not student:
        print("Student Not Found.")
        return

    display_student(student)
    print("Press Enter to keep a current detail. Enter new marks to replace all marks.")
    for field, label in (("roll_number", "Roll number"), ("name", "Name"),
                         ("prn", "PRN"), ("class_name", "Class"),
                         ("division", "Division")):
        value = input(f"{label} [{student[field]}]: ").strip()
        if value:
            student[field] = value

    replace_marks = input("Replace subject marks? (y/n): ").strip().casefold()
    if replace_marks == "y":
        student["marks"] = prompt_marks()
    save_students(students)
    print("Student record updated successfully.")


def list_students(students):
    if not students:
        print("No student records are available.")
        return
    for student in students:
        display_student(student)


def main():
    students = load_students()
    while True:
        print("\nSTUDENT RECORD AND ACADEMIC MANAGEMENT SYSTEM")
        print("1. Add Student")
        print("2. Search Student (Roll Number or PRN)")
        print("3. View All Student Records")
        print("4. Update Student Record")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            search_student(students)
        elif choice == "3":
            list_students(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            print("Records saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 5.")


if __name__ == "__main__":
    main()
