# NOTES
# Incorporate separate for gender, degprog

from errorcatching import check_student_exists, check_org_exists;
from tabulate import tabulate;


def view_filter_role (conn):
    print("Select organization to generate reports:")
    org_name = input("Enter organization name: ")

    if not check_org_exists(conn, org_name):
        print("❌ Organization does not exist!.")
        return
    
    filter_type = 'role'
    filter_value = input(f"Enter {filter_type}: ")

    view_members_by_filter(conn, org_name, filter_type, filter_value)
    return

def view_filter_status (conn):
    print("Select organization to generate reports:")
    org_name = input("Enter organization name: ")

    if not check_org_exists(conn, org_name):
        print("❌ Organization does not exist!.")
        return
    
    filter_type = 'status'
    filter_value = input(f"Enter {filter_type} (Active/Inactive/Alumni): ") #Description to be edited

    view_members_by_filter(conn, org_name, filter_type, filter_value)
    return
    
def view_filter_degprog (conn):
    print("Select organization to generate reports:")
    org_name = input("Enter organization name: ")

    if not check_org_exists(conn, org_name):
        print("❌ Organization does not exist!.")
        return
    
    filter_type = 'degree program'
    filter_value = input(f"Enter {filter_type}: ") #Description to be edited

    view_members_by_filter(conn, org_name, filter_type, filter_value)
    return

def view_filter_batch (conn):
    print("Select organization to generate reports:")
    org_name = input("Enter organization name: ")

    if not check_org_exists(conn, org_name):
        print("❌ Organization does not exist!.")
        return
    
    filter_type = 'batch'
    filter_value = input(f"Enter {filter_type}: ") #Description to be edited

    view_members_by_filter(conn, org_name, filter_type, filter_value)
    return

def view_filter_comm (conn):
    print("Select organization to generate reports:")
    org_name = input("Enter organization name: ")

    if not check_org_exists(conn, org_name):
        print("❌ Organization does not exist!.")
        return
    
    filter_type = 'committee'
    filter_value = input(f"Enter {filter_type}: ") #Description to be edited

    view_members_by_filter(conn, org_name, filter_type, filter_value)
    return

def view_filter_gender(conn):
    print("Select organization to generate reports:")
    org_name = input("Enter organization name: ")

    if not check_org_exists(conn, org_name):
        print("❌ Organization does not exist!.")
        return
    
    filter_type = 'gender'
    filter_value = input(f"Enter {filter_type} (M/F): ")
    if filter_value not in ['M','F']:
        print("❌ Invalid input.")
        return
    try:
        cursor = conn.cursor()
        query = f"""
            SELECT m.student_no, s.first_name, s.last_name, m.acad_year, m.semester, s.{filter_type}
            FROM membership m JOIN student s ON m.student_no = s.student_no
            WHERE m.org_name = ? AND s.{filter_type} = ?
        """
        cursor.execute(query, (org_name, filter_value))
        members = cursor.fetchall()

        if members:
            headers = ["Student no.", "First Name", "Last Name", "Academic Year", "Semester", filter_type.capitalize()]
            print("\n" + tabulate(members, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
        else:
            print("❌ No membership records found.")

    except Exception as e:
        print(f"❌ Error retrieving membership records: {e}")
    finally:
        cursor.close()
    

    return

def view_filter_degprog(conn):
    print("Select organization to generate reports:")
    org_name = input("Enter organization name: ")

    if not check_org_exists(conn, org_name):
        print("❌ Organization does not exist!.")
        return
    
    filter_type = 'degree_program'
    filter_value = input(f"Enter degree program: ")
    try:
        cursor = conn.cursor()
        query = f"""
            SELECT m.student_no, s.first_name, s.last_name, m.acad_year, m.semester, s.{filter_type}
            FROM membership m JOIN student s ON m.student_no = s.student_no
            WHERE m.org_name = ? AND s.{filter_type} = ?
        """
        cursor.execute(query, (org_name, filter_value))
        members = cursor.fetchall()

        if members:
            headers = ["Student no.", "First Name", "Last Name", "Academic Year", "Semester", filter_type.capitalize()]
            print("\n" + tabulate(members, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
        else:
            print("❌ No membership records found.")

    except Exception as e:
        print(f"❌ Error retrieving membership records: {e}")
    finally:
        cursor.close()
    

    return



def view_members_by_filter(conn, org_name, filter_type, filter_value):
    valid_filters = {
        "role": "role",
        "status": "membership_status",
        "batch": "batch",
        "committee": "committee"
    }

    # Ensure the filter type is valid
    if filter_type.lower() not in valid_filters:
        print(f"❌ Invalid filter type: {filter_type}")
        return

    column_name = valid_filters[filter_type.lower()]

    try:
        cursor = conn.cursor()
        query = f"""
            SELECT m.student_no, s.first_name, s.last_name, m.acad_year, m.semester, {column_name}
            FROM membership m JOIN student s ON m.student_no = s.student_no
            WHERE m.org_name = ? AND m.{column_name} = ?
        """
        cursor.execute(query, (org_name, filter_value))
        members = cursor.fetchall()

        if members:
            headers = ["Student no.", "First Name", "Last Name", "Academic Year", "Semester", column_name.capitalize()]
            print("\n" + tabulate(members, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
        else:
            print("❌ No membership records found.")

    except Exception as e:
        print(f"❌ Error retrieving membership records: {e}")
    finally:
        cursor.close()