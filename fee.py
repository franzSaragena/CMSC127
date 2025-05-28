from errorcatching import *
from tabulate import tabulate

def assign_fee(conn):
    student_no = int(input("Enter student number: "))
    
    if not check_student_exists(conn, student_no):
        print("❌ Student not found in the database.")
        return

    org = input("Enter organization name: ").strip()
    
    if not check_org_exists(conn, org):
        print("❌ Org not found in the database.")
        return
    
    if not check_membership_exists(conn, org, student_no, fee_sem):
        print(f"❌ Student with no. {student_no} is not a member of {org}.")
        return
    
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
    print("\nRecord payment.\n")
    try:
        fee_id = int(input("Enter fee ID: "))

        if not check_fee_exists(conn, fee_id):
            print(f"❌ Fee with ID {fee_id} not found in the database.")
            return

        amount_to_add = float(input("Enter amount paid now: "))
        if amount_to_add <= 0:
            print("❌ Amount must be greater than 0.")
            return

        payment_date = input("Enter payment date (YYYY-MM-DD): ").strip()

        cursor = conn.cursor()

        # Get current amount_paid and amount_due
        cursor.execute("SELECT amount_paid, amount_due FROM fee WHERE fee_id = ?", (fee_id,))
        row = cursor.fetchone()

        if row is None:
            print("❌ Fee record could not be retrieved.")
            return

        current_paid = float(row[0])
        amount_due = float(row[1])
        new_total_paid = current_paid + amount_to_add

        if new_total_paid > amount_due:
            print(f"❌ Total paid ({new_total_paid:.2f}) exceeds amount due ({amount_due:.2f}).")
            return

        # Update the record with the new amount and date
        cursor.execute("""
            UPDATE fee
            SET amount_paid = ?, payment_date = ?
            WHERE fee_id = ?
        """, (new_total_paid, payment_date, fee_id))

        conn.commit()
        print(f"✅ Payment recorded. New total paid: {new_total_paid:.2f} / {amount_due:.2f}")

    except ValueError:
        print("❌ Invalid input.")
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
                            CASE is_fully_paid
                                WHEN 1 THEN 'Yes'
                                ELSE 'No'
                            END AS is_fully_paid,
                            amount_paid,
                            payment_date
                        FROM
                            fee
                        WHERE
                            org_name = ?
                       """, (org_name, ))
        results = cursor.fetchall()
        
        if results:
            headers = ["Fee ID", "Student No.", "Amount Due", "Due Date", "Semester", "Is Fully Paid", "Amount Paid", "Payment Date"]
            print("\n" + tabulate(results, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
        else:
            print("❌ No matching fee records found.")
    except Exception as e:
        print(f"❌ Failed to view fees: {e}")
    finally:
        cursor.close()
    