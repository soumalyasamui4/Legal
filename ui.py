import os
import sqlite3

# -------------------------------
# DATABASE SETUP
# -------------------------------
def init_database():
    db_folder = "project_db"
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    db_path = os.path.join(db_folder, "legal_petitions.db")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS petitions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        petitioner TEXT,
        respondent TEXT,
        court_name TEXT,
        case_type TEXT,
        petition_text TEXT
    )
    """)

    conn.commit()
    conn.close()
    return db_path


# -------------------------------
# BACKEND FUNCTION
# -------------------------------
def generate_and_store_petition(db_path, petitioner, respondent, court_name, case_type, facts_list, reliefs_sought):

    facts_text = ""
    for i, f in enumerate(facts_list, 1):
        facts_text += f"{i}. {f}\n"

    relief_text = ""
    for i, r in enumerate(reliefs_sought, 1):
        relief_text += f"{i}. {r}\n"

    petition = f"""
IN THE {court_name.upper()}

CASE TYPE: {case_type.upper()}

PETITIONER: {petitioner}
RESPONDENT: {respondent}

SUBJECT: Petition regarding {case_type}

RESPECTFULLY SHOWETH:

1. That the petitioner is competent to file this petition.
2. That the respondent is connected with the present matter.

FACTS OF THE CASE:
{facts_text}

GROUNDS:
A. The above facts clearly establish cause of action.
B. The actions of the respondent are arbitrary and against natural justice.

RELIEFS SOUGHT:
{relief_text}

PRAYER:
It is humbly prayed that this Hon’ble Court may kindly grant the above reliefs
in the interest of justice.

Place: __________
Date: __________

(Signature)
Petitioner
"""

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO petitions (petitioner, respondent, court_name, case_type, petition_text)
    VALUES (?, ?, ?, ?, ?)
    """, (petitioner, respondent, court_name, case_type, petition))

    conn.commit()
    conn.close()

    return petition


# -------------------------------
# VIEW FUNCTIONS
# -------------------------------
def view_all_petitions(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, petitioner, respondent, case_type FROM petitions")
    data = cur.fetchall()
    conn.close()
    return data


def get_petition_by_id(db_path, pid):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT petition_text FROM petitions WHERE id = ?", (pid,))
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0]
    return "No petition found."


# -------------------------------
# SIMPLE UI (NO INSTALL NEEDED)
# -------------------------------
def console_ui():
    db_path = init_database()

    while True:
        print("\n===== LEGAL PETITION AUTO-DRAFT SYSTEM =====")
        print("1. Generate new petition")
        print("2. View all petitions")
        print("3. View petition by ID")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            petitioner = input("Enter Petitioner Name: ")
            respondent = input("Enter Respondent Name: ")
            court = input("Enter Court Name: ")
            case_type = input("Enter Case Type: ")

            print("\nEnter Facts (type 'done' when finished):")
            facts = []
            while True:
                f = input("> ")
                if f.lower() == "done":
                    break
                facts.append(f)

            print("\nEnter Reliefs (type 'done' when finished):")
            reliefs = []
            while True:
                r = input("> ")
                if r.lower() == "done":
                    break
                reliefs.append(r)

            petition = generate_and_store_petition(
                db_path, petitioner, respondent, court, case_type, facts, reliefs
            )

            print("\n----- GENERATED PETITION -----\n")
            print(petition)

        elif choice == "2":
            rows = view_all_petitions(db_path)
            print("\nStored Petitions:")
            for row in rows:
                print(row)

        elif choice == "3":
            pid = int(input("Enter Petition ID: "))
            print(get_petition_by_id(db_path, pid))

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")


# -------------------------------
# RUN UI
# -------------------------------
if __name__ == "__main__":
    console_ui()