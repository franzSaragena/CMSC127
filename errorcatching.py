import mariadb

def check_student_exists(conn, student_no): # FOR STUDENT NUM CHECKING
    """Returns True if the student exists in the database, False otherwise."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM student WHERE student_no = ?", (student_no,))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        print(f"❌ Error checking student existence: {e}")
        return False
    finally:
        cursor.close()

def check_org_exists(conn, org_name): # FOR ORG NAME CHECKING
    """Returns True if the org exists in the database, False otherwise."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM organization WHERE org_name = ?", (org_name,))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        print(f"❌ Error checking org existence: {e}")
        return False
    finally:
        cursor.close()
def check_membership_exists(conn, org_name, student_no, semester, acad_year=None):
    """Returns True if the membership exists in the database, False otherwise."""
    
    try:
        cursor = conn.cursor()
        
        base_query = """
            SELECT *
            FROM membership
            WHERE org_name = ?
              AND student_no = ?
              AND semester = ?
        """
        params = [org_name, student_no, semester]

        if acad_year is not None:
            base_query += " AND acad_year = ?"
            params.append(acad_year)

        cursor.execute(base_query, params)
        result = cursor.fetchone()
        return result is not None

    except Exception as e:
        print(f"❌ Error checking membership existence: {e}")
        return False
    finally:
        cursor.close()

def check_fee_exists(conn, id):
    """Returns True if the fee exists in the database, False otherwise."""
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fee WHERE fee_id = ?", (id,))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        print(f"❌ Error checking fee existence: {e}")
        return False
    finally:
        cursor.close()