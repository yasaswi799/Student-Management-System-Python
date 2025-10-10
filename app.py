import csv
from tabulate import tabulate
import re

FIELDS = ["RollNo", "FullName", "Age", "Email", "Phone"]
DATABASE_FILE = "students.csv"


def show_menu():
    print("\n==============================")
    print("   Student Management Portal   ")
    print("==============================")
    print("1. Register New Student")
    print("2. Display All Students")
    print("3. Find Student")
    print("4. Modify Student")
    print("5. Remove Student")
    print("6. Exit")
    print("==============================\n")


def validate_input(field, value):
    if field == "RollNo":
        return value.isdigit()
    elif field == "Age":
        return value.isdigit() and 5 <= int(value) <= 100
    elif field == "Email":
        return re.match(r"[^@]+@[^@]+\.[^@]+", value)
    elif field == "Phone":
        return value.isdigit() and len(value) in [10, 11, 12]
    else:
        return True  # FullName can be any string


def register_student():
    print("\n--- Register New Student ---")
    student_info = {}

    # Load existing RollNos to prevent duplicates
    existing_rollnos = set()
    try:
        with open(DATABASE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for student in reader:
                existing_rollnos.add(student["RollNo"].strip())
    except FileNotFoundError:
        pass

    for field in FIELDS:
        while True:
            value = input(f"Enter {field}: ").strip()
            if not validate_input(field, value):
                print(f"❌ Invalid {field}, please try again.")
                continue
            if field == "RollNo" and value in existing_rollnos:
                print("❌ Roll Number already exists! Enter a unique RollNo.")
                continue
            student_info[field] = value
            break

    with open(DATABASE_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(student_info)

    print("✅ Student registered successfully!")


def display_students():
    print("\n--- Student Records ---")
    try:
        with open(DATABASE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            students = list(reader)

            if not students:
                print("⚠️ No student data found.")
                return

            print(tabulate(students, headers="keys", tablefmt="grid"))

    except FileNotFoundError:
        print("⚠️ No records found. Please register a student first.")


def find_student():
    roll = input("Enter Roll Number to search: ").strip()
    found = False

    try:
        with open(DATABASE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for student in reader:
                if student["RollNo"].strip() == roll:
                    print("\n✅ Student Found:")
                    print(tabulate([student], headers="keys", tablefmt="grid"))
                    found = True
                    break
    except FileNotFoundError:
        pass

    if not found:
        print("❌ Student not found.")


def modify_student():
    roll = input("Enter Roll Number to update: ").strip()
    updated_records = []
    modified = False

    try:
        with open(DATABASE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for student in reader:
                if student["RollNo"].strip() == roll:
                    print("Enter new details (leave blank to keep existing):")
                    for field in FIELDS:
                        new_value = input(f"{field} ({student[field]}): ").strip()
                        if new_value:
                            if validate_input(field, new_value):
                                student[field] = new_value
                            else:
                                print(f"❌ Invalid {field}, keeping existing value.")
                    modified = True
                updated_records.append(student)

        if modified:
            with open(DATABASE_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(updated_records)
            print("✅ Student details updated successfully!")
        else:
            print("❌ Student not found.")

    except FileNotFoundError:
        print("⚠️ No data available to update.")


def remove_student():
    roll = input("Enter Roll Number to delete: ").strip()
    updated_records = []
    deleted = False

    try:
        with open(DATABASE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for student in reader:
                if student["RollNo"].strip() != roll:
                    updated_records.append(student)
                else:
                    deleted = True

        if deleted:
            with open(DATABASE_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(updated_records)
            print(f"✅ Student with Roll No. {roll} deleted successfully.")
        else:
            print("❌ Student not found.")

    except FileNotFoundError:
        print("⚠️ No data available to delete.")


if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            register_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            find_student()
        elif choice == "4":
            modify_student()
        elif choice == "5":
            remove_student()
        elif choice == "6":
            print("\n👋 Thank you for using the Student Management Portal. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice, please try again.")