from tabulate import tabulate

def add_org(conn):
    org_name = input("Enter organization name: ")

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO organization (org_name)
            VALUES (?)
        """, (org_name,))
        conn.commit()
        print("✅ Organization added successfully.")
    except Exception as e:
        print(f"❌ Failed to add organization: {e}")
    finally:
        cursor.close()
        
def delete_org(conn):
    org_name = input("Enter organization name: ")
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM organization
            WHERE org_name = ?
        """, (org_name,))
        conn.commit()
        print("✅ Organization deleted successfully.")
    except Exception as e:
        print(f"❌ Failed to delete organization: {e}")
    finally:
        cursor.close()

def update_org(conn):
    org_name = input("Enter organization name: ")
    new_name = input("Enter new organization name: ")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE organization
            SET org_name = ?
            WHERE org_name =  ?
        """, (new_name, org_name))
        conn.commit()
        print("✅ Organization name updated successfully.")
    except Exception as e:
        print(f"❌ Failed to update organization name: {e}")
    finally:
        cursor.close()

def view_all(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT org_name Organization FROM organization ORDER BY org_name ASC")
        orgs = cursor.fetchall()
        if not orgs:
            print("No organizations found.")
            return
        print("/n"+tabulate(orgs, headers=["Registered Organizations"], tablefmt="grid", numalign="center", stralign="center"))
    except Exception as e:
        print(f"❌ Error retrieving organizations: {e}")
    finally:
        cursor.close()