# NOTES
# remove_member not working yet,
# RESOLVE: should we delete fees/fee history upon removing a member?

import mariadb
from tabulate import tabulate

def add_member(conn):
    student_no = int(input("Enter student no.:  "))
    org_name = input("Enter organization name: ").strip()
    acad_year = input("Enter academic year (yyyy-yyyy): ").strip()
    semester = int(input("Enter semester (1/2): "))
    role = input("Enter role: ").strip().capitalize()
    committee = input("Enter committee: ").strip().capitalize()
    batch = int(input("Enter batch: "))
    status = input("Enter status (Active, Inactive, Expelled, Suspended, Alumni): ").strip().capitalize()
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO membership
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_no, org_name, acad_year, semester, role, committee, batch, status))
        conn.commit()
        print("✅ Successfully added student as a member.")
    except mariadb.IntegrityError as e:
        msg = str(e).lower()
        if "foreign key constraint fails" in msg:
            if "student_no" in msg:
                print("❌ Cannot add member: Student with this student number does not exist.")
            elif "org_name" in msg:
                print("❌ Cannot add member: Organization with this name does not exist.")
            else:
                print("❌ Cannot add member: One of the linked records does not exist.")
        elif "duplicate entry" in msg:
            print("❌ This student is already a member of that organization.")
        else:
            print("❌ Invalid data. Please check your input.")

    except mariadb.Error as e:
        print("❌ A database error occurred.")
        print(f"[DEBUG] {e}")
    except Exception as e:
        print(f"❌ Failed to add student as a member: {e}")
    finally:
        cursor.close()
        
def remove_member(conn):
    student_no = int(input("Enter student no.:  "))
    org_name = input("Enter organization name: ").strip()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM membership
            WHERE
                student_no = ? 
                AND org_name = ?            
        """, (student_no, org_name))
        conn.commit()
        print("✅ Successfully removed student as a member.")
    except Exception as e:
        print(f"❌ Failed to remove student as a member: {e}")
    finally:
        cursor.close()
        
def update_membership(conn):
    print("Select membership to update. ")
    
    student_no = int(input("Enter student no.: "))
    org = input("Enter current organization name: ").strip()
    year = input("Enter current academic year (yyyy-yyyy): ").strip()
    semester = int(input("Enter current semester (1/2): "))
    committee = input("Enter current committee: ").strip().capitalize()
    role = input("Enter current role: ").strip()

    print("\nLeave a field blank if you don't want to update it.")

    new_status = input("Enter new membership status (e.g., Active, Inactive): ").strip().capitalize()
    new_role = input("Enter new role (e.g., Member, President): ").strip().capitalize()
    new_committee = input("Enter new committee (e.g., Finance, Logistics): ").strip().capitalize()

    updates = []
    params = []

    if new_status:
        updates.append("membership_status = ?")
        params.append(new_status)
    if new_role:
        updates.append("role = ?")
        params.append(new_role)
    if new_committee:
        updates.append("committee = ?")
        params.append(new_committee)

    if not updates:
        print("⚠️ No fields provided for update.")
        return

    # Add WHERE clause parameters
    params.extend([student_no, org, year, semester, committee, role])

    try:
        cursor = conn.cursor()
        query = f"""
            UPDATE membership
            SET {', '.join(updates)}
            WHERE student_no = ? AND org_name = ? AND acad_year = ? AND semester = ? AND committee = ? AND role = ?
        """
        cursor.execute(query, params)
        if cursor.rowcount == 0:
            print("❌ No matching membership record found.")
        else:
            conn.commit()
            print("✅ Membership details updated.")
    except Exception as e:
        print(f"❌ Error updating membership: {e}")
    finally:
        cursor.close()
        
def search_member(conn):
    print("""
        [1] Search by student number
        [2] Search by student name      
    """)
    
    try:
        choice = int(input("Choose method: "))
    except ValueError:
        print("❌ Invalid input.")
        return

    try:
        cursor = conn.cursor()
        if choice == 1:
            student_no = int(input("Enter student number: "))
            query = """
                SELECT student_no, s.first_name, s.last_name, s.gender, s.degree_program, m.org_name, m.acad_year, m.semester, m.role, m.committee, m.batch, m.membership_status
                FROM student s
                NATURAL JOIN membership m
                WHERE s.student_no = ?
                ORDER BY m.acad_year, m.semester
            """
            cursor.execute(query, (student_no,))
        
        elif choice == 2:
            name = input("Enter name (partial OK): ").strip().capitalize()
            query = """
                SELECT student_no, s.first_name, s.last_name, s.gender, s.degree_program, m.org_name, m.acad_year, m.semester, m.role, m.committee, m.batch, m.membership_status
                FROM student s
                NATURAL JOIN membership m
                WHERE s.first_name LIKE ? OR s.last_name LIKE ?
                ORDER BY s.student_no, m.acad_year, m.semester
            """
            cursor.execute(query, (name, name))
        
        else:
            print("❌ Invalid choice.")
            return
        
        memberships = cursor.fetchall()
        if memberships:
            headers = ["Student no.", "First Name", "Last Name", "Gender", "Degree Program", "Org Name", "Academic Year", "Semester", "Role", "Committee", "Batch", "Status" ]
            
            print("\n" + tabulate(memberships, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
        else:
            print("❌ No matching membership record found.")
            
        
    except Exception as e:
        print(f"❌ Error during search: {e}")
    finally:
        cursor.close()
    
def view_all_memberships(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT m.student_no, m.org_name, m.acad_year, m.semester, m.role, m.committee, m.batch, m.membership_status
                       FROM membership m
                       """)
        memberships = cursor.fetchall()
        if memberships:
            headers = ["Student no.", "Org Name", "Academic Year", "Semester", "Role", "Committee", "Batch", "Status" ]
            print("\n" + tabulate(memberships, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
        else:
            print("❌ No membership records found.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        