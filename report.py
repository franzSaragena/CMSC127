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

# [7] Members with unpaid fees (by org/semester/year)
def view_unpaid_members(conn):
    print("View members with unpaid fees (by organization, semester, and academic year)")

    org_name = input("Enter organization name: ").strip()
    semester = input("Enter semester: ").strip()
    acad_year = input("Enter academic year (YYYY-YYYY): ").strip()

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT
                s.student_no,
                s.first_name,
                s.last_name,
                m.role,
                m.committee,
                m.membership_status,
                f.amount_due,
                f.amount_paid
            FROM
                student s
            JOIN membership m ON s.student_no = m.student_no
            JOIN fee f ON s.student_no = f.student_no AND m.org_name = f.org_name
            WHERE
                m.org_name = ?
                AND m.semester = ?
                AND m.acad_year = ?
                AND f.fee_semester = m.semester
                AND f.amount_due > f.amount_paid
            ORDER BY
                s.last_name, s.first_name
        """, (org_name, semester, acad_year))

        rows = cursor.fetchall()

        if rows:
            headers = ["Student No", "First Name", "Last Name", "Role", "Committee", "Status", "Amount Due", "Amount Paid"]
            print(tabulate(rows, headers=headers, tablefmt="grid", stralign="center"))
        else:
            print("No members with unpaid fees found for the given criteria.")
    except Exception as e:
        print(f"❌ Failed to retrieve unpaid members: {e}")
    finally:
        cursor.close()
    
# [8] A member's unpaid fees across all orgs (Member POV)
def view_member_unpaid_fees(conn):
    print("View a member's unpaid fees across all organizations.")
    student_no = input("Enter student number: ").strip()

    query = """
        SELECT
            f.org_name,
            m.acad_year,
            m.semester,
            f.amount_due,
            f.amount_paid,
            f.due_date,
            f.payment_date
        FROM 
            fee f
        JOIN membership m
            ON f.student_no = m.student_no AND f.org_name = m.org_name
        WHERE 
            f.student_no = ?
            AND f.amount_due > f.amount_paid
        ORDER BY 
            f.org_name, m.acad_year DESC, m.semester DESC;
    """

    try:
        cursor = conn.cursor()
        cursor.execute(query, (student_no,))
        results = cursor.fetchall()

        if results:
            headers = ["Organization", "Academic Year", "Semester", "Amount Due", "Amount Paid", "Due Date", "Payment Date"]
            print("\n" + tabulate(results, headers=headers, tablefmt="grid", numalign="right", stralign="center"))
        else:
            print("✅ No unpaid fees found for this member.")
    except Exception as e:
        print(f"❌ Failed to retrieve unpaid fees: {e}")
    finally:
        cursor.close()

        
# [9] Late payments (by org/semester/year)
def view_late_payments(conn):
    print("View late payments by organization, semester, and academic year.")
    org_name = input("Enter organization name: ").strip()
    semester = input("Enter semester: ").strip()
    acad_year = input("Enter academic year (YYYY-YYYY): ").strip()

    query = """
        SELECT
            s.student_no,
            s.first_name,
            s.last_name,
            f.amount_due,
            f.amount_paid,
            CASE f.is_fully_paid
                WHEN 1 THEN 'Yes'
                ELSE 'No'
            END AS is_fully_paid,
            f.due_date,
            f.payment_date
        FROM fee f
        JOIN membership m ON f.student_no = m.student_no AND f.org_name = m.org_name
        JOIN student s ON f.student_no = s.student_no
        WHERE f.org_name = ?
            AND m.semester = ?
            AND m.acad_year = ?
            AND f.payment_date IS NOT NULL
            AND f.payment_date > f.due_date
        ORDER BY f.payment_date DESC;
    """

    try:
        cursor = conn.cursor()
        cursor.execute(query, (org_name, semester, acad_year))
        results = cursor.fetchall()

        if results:
            headers = ["Student No", "First Name", "Last Name", "Amount Due", "Amount Paid", "Is Fully Paid", "Due Date", "Payment Date"]
            print(f"\nLate Payments for {org_name} - {semester}S {acad_year}\n")
            print(tabulate(results, headers=headers, tablefmt="grid", numalign="right", stralign="center"))
        else:
            print(f"✅ No late payments found for {org_name} {semester} {acad_year}.")
    except Exception as e:
        print(f"❌ Failed to retrieve late payments: {e}")
    finally:
        cursor.close()

        
# [10] Members with highest debt (by org/semester)
def view_members_highest_debt(conn):
    print("View members with the highest debt by organization, semester, and academic year")
    org_name = input("Enter organization name: ").strip()
    semester = input("Enter semester: ").strip()
    acad_year = input("Enter academic year (YYYY-YYYY): ").strip()

    try:
        cursor = conn.cursor()
        query = """
            WITH member_debts AS (
                SELECT
                    s.student_no,
                    s.first_name,
                    s.last_name,
                    SUM(f.amount_due - f.amount_paid) AS total_debt
                FROM student s
                JOIN membership m ON s.student_no = m.student_no
                JOIN fee f ON m.student_no = f.student_no
                        AND m.org_name = f.org_name
                WHERE
                    m.org_name = ?
                    AND m.semester = ?
                    AND m.acad_year = ?
                    AND (f.amount_due - f.amount_paid) > 0
                GROUP BY s.student_no
            ),
            max_debt AS (
                SELECT MAX(total_debt) AS highest_debt FROM member_debts
            )
            SELECT
                student_no,
                first_name,
                last_name,
                total_debt
            FROM member_debts
            WHERE total_debt = (SELECT highest_debt FROM max_debt)
            ORDER BY student_no;
        """

        cursor.execute(query, (org_name, semester, acad_year))
        results = cursor.fetchall()

        if results:
            headers = ["Student No", "First Name", "Last Name", "Total Debt"]
            print("\n" + tabulate(results, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
        else:
            print("✅ No members with unpaid fees found.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()

def view_executive(conn):
    print("View all executive committee members of a given organization for a given academic year")
    org_name = input("Enter organization name: ").strip()
    acad_year = input("Enter academic year (YYYY-YYYY): ").strip()
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
                        SELECT
                            s.student_no,
                            s.first_name,
                            s.last_name,
                            m.role,
                            m.semester
                        FROM
                            student s
                        NATURAL JOIN
                            membership m
                        WHERE
                            m.org_name=?
                            AND m.committee="Executive"
                            AND m.acad_year=?
                       """, (org_name, acad_year))
        results = cursor.fetchall()
        
        if results:
            headers = ["Student Number", "First Name", "Last Name", "Role", "Semester"]
            print("\n" + tabulate(results, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
        else:
            print("❌ No data found. ")

            
    except Exception as e:
        print(f"❌ Failed to view executive members: {e}")
    finally:
        cursor.close()
        
def view_presidents(conn):
    print("View all presidents (or any other role) within an organization.")
    org_name = input("Enter organization name: ").strip()
    role = input("Enter role (e.g. President): ").strip().capitalize()
      
    try:
        cursor = conn.cursor()
        cursor.execute("""
                        SELECT
                            s.student_no,
                            s.first_name,
                            s.last_name,
                            m.acad_year,
                            m.semester
                        FROM
                            student s
                        NATURAL JOIN
                            membership m
                        WHERE
                            m.org_name=?
                            AND role=?
                        ORDER BY
                            m.acad_year DESC
                       """, (org_name, role))
        results = cursor.fetchall()
        
        if results:
            headers = ["Student Number", "First Name", "Last Name", "Academic Year", "Semester"]
            print("\n" + tabulate(results, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Exception as e:
        print(f"❌ Failed to view {role}s: {e}")
    finally:
        cursor.close()

def get_active_inactive_percentage(conn):
    print("Percentage of active vs inactive members")
    org_name = input("Enter organization name: ").strip()
    n = int(input("Enter number of semesters to include (n): "))
    
    query = f"""
    WITH recent_semesters AS (
        SELECT DISTINCT acad_year, semester
        FROM membership
        WHERE org_name = ?
        ORDER BY acad_year DESC, semester DESC
        LIMIT ?
    )
    SELECT
        m.acad_year,
        m.semester,
        m.membership_status,
        COUNT(*) AS member_count,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY m.acad_year, m.semester), 2) AS percentage
    FROM membership m
    JOIN recent_semesters r
      ON m.acad_year = r.acad_year AND m.semester = r.semester
    WHERE m.org_name = ?
    GROUP BY m.acad_year, m.semester, m.membership_status
    ORDER BY m.acad_year DESC, m.semester DESC;
    """
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, (org_name, n, org_name))
        results = cursor.fetchall()
        
        if results:
            headers = ["Academic Year", "Semester", "Status", "Count", "Percentage"]
            print("\n" + tabulate(results, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
        else:
            print("❌ No records found.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        
        
def get_org_fee_summary(conn):
    org_name = input("Enter organization name: ").strip()
    date = input("Enter date (YYYY-MM-DD): ").strip()
    
    print(f"Total Amount of Unpaid and Paid Fees As of {date}")
    try:
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT
                        SUM(CASE 
                            WHEN payment_date IS NOT NULL AND payment_date <= ? THEN amount_paid
                            ELSE 0
                        END) AS total_paid,

                        SUM(CASE 
                            WHEN due_date <= ? AND (payment_date IS NULL OR payment_date > ?) THEN amount_due - amount_paid
                            ELSE 0
                        END) AS total_unpaid
                    FROM fee
                    WHERE org_name = ?
                       """, (date, date, date, org_name))
        results = cursor.fetchall()
        
        if results:
            headers = ["Total Amount Paid", "Total Amount Unpaid"]
            print("\n" + tabulate(results, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Exception as e:
        print(f"❌ Error during viewing fee summary: {e}")
    finally:
        cursor.close()

def view_alumni(conn):
    org_name = input("Enter organization name: ").strip()
    date = input("Enter date (YYYY-MM-DD): ").strip()

    as_of_year = int(date[:4])  # Extract year from input string

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.student_no, s.first_name, s.last_name, m.acad_year, m.semester,
                   m.role, m.committee, m.batch
            FROM membership m
            JOIN student s ON m.student_no = s.student_no
            WHERE m.org_name = ?
              AND m.membership_status = 'Alumni'
        """, (org_name,))
        rows = cursor.fetchall()

        filtered = []
        for row in rows:
            acad_year_start = int(row[3][:4])  # Extract start year from 'YYYY-YYYY'
            if acad_year_start <= as_of_year:
                filtered.append(row)

        if not filtered:
            print(f"❌ No alumni members found for '{org_name}' as of {as_of_year}.")
            return

        headers = ["Student No.", "First Name", "Last Name", "Academic Year", "Semester", "Role", "Committee", "Batch"]
        print(f"\nAlumni Members of '{org_name}' as of {date}")
        print("\n" + tabulate(filtered, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Exception as e:
        print(f"❌ Error: {e}")
