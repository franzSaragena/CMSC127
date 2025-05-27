import mariadb
import org, membership, fee, reports, student

# === DATABASE CONNECTION ===

def grant_privileges():
    print("Admin access required for setting up...")
    
    root_user = input("Enter admin username (e.g., root): ").strip()
    root_pass = input("Enter admin password: ").strip()
    
    target_user = input("Enter app username to grant access to: ").strip()
    target_pass = input(f"Enter password for user '{target_user}': ").strip()
    db_name = "student_org_db"
    
    try:
        # Connect as root (or another admin user)
        admin_conn = mariadb.connect(
            user=root_user,
            password=root_pass,
            host="localhost",
            port=3306
        )
        admin_cursor = admin_conn.cursor()
        
        # Create database if it does not exists
        admin_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

        # Create user if it doesn't exists // ADDED : Franz
        admin_cursor.execute(
            f"CREATE USER IF NOT EXISTS '{target_user}'@'localhost' IDENTIFIED BY '{target_pass}'"
        )
        admin_cursor.execute(
            f"CREATE USER IF NOT EXISTS '{target_user}'@'%' IDENTIFIED BY '{target_pass}'"
        )

        # Grant privileges for both localhost and any-host
        admin_cursor.execute(
            f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{target_user}'@'localhost' IDENTIFIED BY '{target_pass}'"
        )
        admin_cursor.execute(
            f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{target_user}'@'%' IDENTIFIED BY '{target_pass}'"
        )
        admin_cursor.execute("FLUSH PRIVILEGES")

        print(f"✅ Privileges granted to user '{target_user}' on '{db_name}'.")
        
        return target_user, target_pass, db_name

    except mariadb.Error as e:
        print(f"❌ Admin setup failed: {e}")
    finally:
        admin_cursor.close()
        admin_conn.close()

def setup_db(user, password, db_name):
    try:
        conn = mariadb.connect(
            user=user,
            password=password,
            host="localhost",
            port=3306,
            database=db_name
        )
        cursor = conn.cursor()
        # Create tables if they don't exist
        
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS student (
                        student_no INT(9) NOT NULL PRIMARY KEY,
                        first_name VARCHAR(30) NOT NULL,
                        last_name VARCHAR(30) NOT NULL,
                        gender VARCHAR(6) NOT NULL,
                        degree_program VARCHAR(4) NOT NULL
                    )
                        """)
        
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS organization (
                        org_name VARCHAR(100) NOT NULL PRIMARY KEY
                    )
                        """)

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS membership (
                        student_no INT(9) NOT NULL,
                        org_name VARCHAR(100) NOT NULL,
                        acad_year CHAR(9) NOT NULL,
                        semester INT(1) NOT NULL,
                        role VARCHAR(50) NOT NULL,
                        committee VARCHAR(100) NOT NULL,
                        batch INT(4) NOT NULL,
                        membership_status VARCHAR(9) NOT NULL,
                        CONSTRAINT membership_student_no_fk FOREIGN KEY(student_no) REFERENCES student(student_no),
                        CONSTRAINT membership_org_name_fk FOREIGN KEY(org_name) REFERENCES organization(org_name),
                        PRIMARY KEY(student_no, org_name, acad_year, semester, role, committee, batch, membership_status)
                    )    
                        """)
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fee (
                        fee_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        student_no INT(9) NOT NULL,
                        org_name VARCHAR(100) NOT NULL,
                        amount_due DECIMAL(5,2) NOT NULL,
                        due_date DATE NOT NULL,
                        fee_semester INT(1) NOT NULL,
                        is_fully_paid BOOLEAN GENERATED ALWAYS AS (amount_paid = amount_due) STORED,
                        amount_paid DECIMAL(5,2) NOT NULL DEFAULT 0,
                        payment_date DATE DEFAULT NULL,
                        CONSTRAINT fee_student_org_fk FOREIGN KEY(student_no, org_name) REFERENCES membership(student_no, org_name)
                    )               
                        """)
        conn.commit()
        return conn
    except mariadb.Error as e:
        print(f"❌ Error connecting as target user")
        return None
    
# === COMMON ===

def prompt_return():
    input("\nPress Enter to continue...")


# === MENU DISPLAYS ===

def display_main_menu():
    print("""
====== Student Organization Management System ======

[1] Students
[2] Organizations
[3] Memberships
[4] Fees
[5] Reports

[0] Exit
""")

def display_student_menu():
    print("""
🙋‍♀️ STUDENT MANAGEMENT

  [1] Add a student
  [2] View all students
  [3] Delete a student
  [4] Update student information
  
  [0] Back to Main Menu
""")

def display_org_menu():
    print("""
🏛️  ORGANIZATION MANAGEMENT

  [1] Add organization
  [2] View all organizations
  [3] Delete an organization
  [4] Update organization name
  
  [0] Back to Main Menu
""")


def display_membership_menu():
    print("""
📁  MEMBERSHIP MANAGEMENT

  [1] Add student to organization
  [2] Remove student from organization
  [3] Update membership details (status, role, committee)
  [4] Search for a member (by student number or name)
  [5] View all memberships
  
  [0] Back to Main Menu
""")


def display_fee_menu():
    print("""
💰  FEES MANAGEMENT

  [1] Assign fee to member
  [2] Record payment
  [3] View all org fees
  
  [0] Back to Main Menu
""")



def display_reports_menu():
    print("""
📊  REPORTS
  
  -- Member Breakdown --
  [1] Members by role
  [2] Members by status
  [3] Members by gender
  [4] Members by degree program
  [5] Members by batch
  [6] Members by committee
  [7] Alumni Members

  -- Fee and Payment Insights --
  [8] Members with unpaid fees (by org/semester/year)
  [9] A member's unpaid fees across all orgs (Member POV)
 [10] Late payments (by org/semester/year)
 [11] Members with highest debt (by org/semester)

  -- Leadership and History --
 [12] Executive committee members (by org/year)
 [13] Presidents by org (chronological)
 
  -- Statistics --
 [14] Active vs inactive members over N semesters
 [15] Total paid and unpaid fees (as of a date)
 
 [0] Back to Main Menu
""")

def run_menu_loop(menu_display_func, command_dict, back_option=0, conn=None):
    """
    Runs a menu using a display function and a command dispatch dictionary.

    Parameters:
    - menu_display_func: function that prints the menu
    - command_dict: {int: function} mapping user input to callable actions
    - back_option: int value that exits the menu (default = 0)
    - conn: passed to each command function
    """
    while True:
        menu_display_func()
        try:
            choice = int(input("Select an option: "))
        except ValueError:
            print("❌ Invalid input. Enter a number.")
            continue

        if choice == back_option:
            break

        action = command_dict.get(choice)
        if action:
            action(conn)
        else:
            print("⚠️ Invalid option.")

        input("\nPress Enter to continue...")

# === MENU HANDLERS ===
def handle_student(conn):
    student_commands = {
        1: student.add_student,
        2: student.view_all,
        3: student.remove_student,
        4: student.update_student
    }
    
    run_menu_loop(display_student_menu, student_commands, conn=conn)
    
# -- MEMBERSHIP HANDLER --
def handle_org(conn):
    org_commands = {
        1: org.add_org,
        2: org.view_all,
        3: org.delete_org,
        4: org.update_org
    }
     
    run_menu_loop(display_org_menu, org_commands, conn=conn)
        
# -- MEMBERSHIP HANDLER --
def handle_membership(conn):
    mem_commands = {
        1: membership.add_member,
        2: membership.remove_member,
        3: membership.update_membership,
        4: membership.search_member,
        5: membership.view_all_memberships
    }
     
    run_menu_loop(display_membership_menu, mem_commands, conn=conn)


# -- FEE HANDLER --

def handle_fee_management(conn):
    fee_commands = {
        1: fee.assign_fee,
        2: fee.record_payment,
        3: fee.view_all
    }

    run_menu_loop(display_fee_menu, fee_commands, conn=conn)


# -- REPORT HANDLER --

def handle_reports(conn):
    report_commands = {
        7: reports.view_alumni,
        11: reports.view_executive,
        12: reports.view_presidents,
        13: reports.get_active_inactive_percentage,
        14: reports.get_org_fee_summary
    }

    run_menu_loop(display_reports_menu, report_commands, conn=conn)


# -- EXIT HANDLER --
def exit_program(conn):
    print("Exiting program...")
    conn.close()
    exit()


# === DISPATCH DICTIONARY FOR MAIN MENU ===

main_commands = {
    0: exit_program,
    1: handle_student,
    2: handle_org,
    3: handle_membership,
    4: handle_fee_management,
    5: handle_reports
}


# === MAIN LOOP ===

def main():
    print("Login with your application user:")
    user = input("Username: ").strip()
    password = input("Password: ").strip()
    db_name = "student_org_db"

    conn = setup_db(user, password, db_name)

    if not conn:
        choice = input("Do you want to grant privileges and set up the system as admin? (y/n): ").strip().lower()
        if choice == "y":
            user, password, db_name = grant_privileges()
            conn = setup_db(user, password, db_name)
            if not conn:
                print("❌ Setup failed. Exiting.")
                return
        else:
            print("❌ Cannot continue without access. Exiting.")
            return

    print("✅ Connected successfully. Launching system...")

    while True:
        display_main_menu()
        try:
            choice = int(input("Select an option: "))
        except ValueError:
            print("❌ Invalid input. Enter a number.")
            continue

        action = main_commands.get(choice)
        if action:
            action(conn)
        else:
            print("⚠️ Invalid selection.")


if __name__ == "__main__":
    main()
