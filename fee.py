# NOT YET TESTED
from errorcatching import check_student_exists;

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

def update_fee(conn):
    print("Select fee to update.")
    fee_id = int(input("Enter fee ID: "))

    print("\nLeave a field blank if you don't want to update it.")

    # Dictionary of field names and input prompts
    fields = {
        "student_no": "Enter new student number: ",
        "org_name": "Enter new organization name: ",
        "amount_due": "Enter new amount due: ",
        "due_date": "Enter new due date (YYYY-MM-DD): ",
        "fee_semester": "Enter new semester (1/2): ",
        "amount_paid": "Enter new amount paid: ",
        "payment_date": "Enter new payment date (YYYY-MM-DD): "
    }

    updates = []
    params = []

    for column, prompt in fields.items():
        user_input = input(prompt).strip()
        if user_input != "":
            # Convert to correct type if necessary
            if column in ["student_no", "fee_semester"]:
                user_input = int(user_input)
            elif column in ["amount_due", "amount_paid"]:
                user_input = float(user_input)
            # Else, keep as string (e.g., dates and org_name)
            updates.append(f"{column} = ?")
            params.append(user_input)

    if not updates:
        print("⚠️ No fields to update. Operation cancelled.")
        return

    try:
        cursor = conn.cursor()
        sql = f"UPDATE fee SET {', '.join(updates)} WHERE fee_id = ?"
        params.append(fee_id)
        cursor.execute(sql, params)
        conn.commit()
        print("✅ Fee updated successfully.")
    except Exception as e:
        print(f"❌ Failed to update fee: {e}")
    finally:
        cursor.close()

        
    