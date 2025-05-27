from tabulate import tabulate

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
        conn.commit()
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
        conn.commit()
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
            headers = ["Academic Year", "Semster", "Academic Year", "Status", "Count", "Percentage"]
            print("\n" + tabulate(results, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
        else:
            print("❌ No records found.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        
        
def get_org_fee_summary(conn):
    print("Total Amount of Unpaid and Paid Fees")
    org_name = input("Enter organization name: ").strip()
    date = input("Enter date (YYYY-MM-DD): ").strip()
    
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
        conn.commit()
    except Exception as e:
        print(f"❌ Error during viewing fee summary: {e}")
    finally:
        cursor.close()