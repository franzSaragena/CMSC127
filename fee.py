# NOT YET TESTED
from errorcatching import check_student_exists
from tabulate import tabulate

def assign_fee(conn):
    student_no = int(input("Enter student number: "))
    if not check_student_exists(conn, student_no): # CATCH NON EXISTENT STUDENT
        print("❌ Student not found in the database.")
        return


    org = input("Enter organization name: ").strip()
    amount_due = float(input("Enter amount due: "))
    due_date = input("Enter due date (YYYY-MM-DD): ").strip()
    fee_sem = int(input("Enter the semester number the fee is for (e.g., 1 for 1st semester): "))

    try:
        cursor = conn.cursor()
        #ONLY INSERT ONCE RESULT EXISTS
        cursor.execute("""
                       INSERT into fee (student_no, org_name, amount_due, due_date, fee_semester)
                       VALUES (?, ?, ?, ?, ?)
                       """, (student_no, org, amount_due, due_date, fee_sem))
        conn.commit()
        print("✅ Fee assigned successfully.")
    except Exception as e:
        print(f"❌ Failed to assign fee: {e}")
    finally:
        cursor.close()

def remove_fee(conn):
    print("Select fee to be removed.")
    fee_id = int(input("Enter fee id of fee to be removed: "))
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fee WHERE fee_id = ?", (fee_id))
        conn.commit()
        print("✅ Fee removed successfully.")
    except Exception as e:
        print(f"❌ Failed to remove fee: {e}")
    finally:
        cursor.close()
        
def record_payment(conn):
    fee_id = int(input("Enter fee id: "))
    amount_paid = float(input("Enter amount paid: "))
    payment_date = input("Enter payment date (YYYY-MM-DD): ").strip()
    
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE fee SET amount_paid = ?, payment_date = ? WHERE fee_id = ?", (amount_paid, payment_date, fee_id))
        conn.commit()
        print("✅ Payment recorded successfully.")
    except Exception as e:
        print(f"❌ Failed to record payment: {e}")
    finally:
        cursor.close()

def view_all(conn):
    print("View all fees by org")
    org_name = input("Enter organization name: ").strip()
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT
                            fee_id,
                            student_no,
                            amount_due,
                            due_date,
                            fee_semester,
                            is_fully_paid,
                            amount_paid,
                            payment_date
                        FROM
                            fee
                        WHERE
                            org_name = ?
                       """, (org_name, ))
    except Exception as e:
        print(f"❌ Failed to view fees: {e}")
    finally:
        cursor.close()
    