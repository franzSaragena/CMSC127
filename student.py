from errorcatching import check_student_exists
from tabulate import tabulate

def add_student(conn):
    student_no = input("Enter student No: ")
    if check_student_exists(conn,student_no): # Doesnt allow creation of already existing student no.
        print("❌ Student with existing student number already exists.")
        return

    fname = input("Enter first name: ").strip().capitalize()
    lname = input("Enter last name: ").strip().capitalize()
    gender = input("Enter gender (Male/Female): ").strip().capitalize()
    degree = input("Enter degree program: ").strip().capitalize()

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO student (student_no, first_name, last_name, gender, degree_program)
            VALUES (?, ?, ?, ?, ?)
        """, (student_no, fname, lname, gender, degree))
        conn.commit()
        print("✅ Student added successfully.")
    except Exception as e:
        print(f"❌ Failed to add student: {e}")
    finally:
        cursor.close()

def view_all(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT student_no, first_name, last_name, gender, degree_program FROM student")
        students = cursor.fetchall()
        if students:
            headers = ["Student no.", "First Name", "Last Name", "Gender", "Degree Program"]
            print("\n" + tabulate.tabulate(students, headers=headers, tablefmt="grid", numalign="center", stralign="center"))

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        
        return


def remove_student(conn):
    print("Select student to be removed.")
    student_id = input("Enter student ID of student to be removed:")

    if not check_student_exists(conn, student_id):
        print("❌ Student doesn't exists.")
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE student_no = ?", (student_id))
        conn.commit()
    except Exception as e:
        print(f"❌ failed to remove student : {e}")
    return


def update_student(conn):
    print("Select student to be updated.")
    student_no = input("Enter student number of student to be updated:").strip()

    # Validate student existence early and exit if not found
    if not check_student_exists(conn, student_no):
        print("❌ Student doesn't exist.")
        return

    print("\nLeave a field blank if you don't want to update it.")

    # Dictionary of field names and input prompts
    fields = {
        "first_name": "Enter new first name: ",
        "last_name": "Enter new last name: ",
        "gender": "Enter gender (Male/Female): ",
        "degree_program": "Enter new degree program: "
    }

    updates = []
    params = []

    for column, prompt in fields.items():
        user_input = input(prompt).strip()
        if user_input != "":
            updates.append(f"{column} = ?")
            params.append(user_input)

    if not updates:
        print("⚠️ No fields to update. Operation cancelled.")
        return

    try:
        cursor = conn.cursor()
        sql = f"UPDATE student SET {', '.join(updates)} WHERE student_no = ?"
        params.append(student_no)  # use student_no, not student_id
        cursor.execute(sql, params)
        conn.commit()
        print("✅ Student updated successfully.")
    except Exception as e:
        print(f"❌ Failed to update student: {e}")
    finally:
        cursor.close()
    return