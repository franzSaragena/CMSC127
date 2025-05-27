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
