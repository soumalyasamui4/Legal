import os
import sqlite3

# -------------------------------
# DATABASE SETUP (ROBUST)
# -------------------------------
def init_database():
    # create a safe writable folder
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
# MAIN FUNCTION
# -------------------------------
def generate_and_store_petition(db_path, petitioner, respondent, court_name, case_type, facts_list, reliefs_sought):
    # convert lists to bullet format
    facts_text = ""
    for i, f in enumerate(facts_list, 1):
        facts_text += f"{i}. {f}\n"

    relief_text = ""
    for i, r in enumerate(reliefs_sought, 1):
        relief_text += f"{i}. {r}\n"

    # petition draft
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
    INSERT INTO petitions(petitioner, respondent, court_name, case_type, petition_text)
    VALUES (?, ?, ?, ?, ?)
    """, (petitioner, respondent, court_name, case_type, petition))

    conn.commit()
    conn.close()

    return petition


# -------------------------------
# VIEW ALL PETITIONS
# -------------------------------
def view_all_petitions(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT id, petitioner, respondent, case_type FROM petitions")
    rows = cur.fetchall()

    conn.close()
    return rows


# -------------------------------
# VIEW ONE PETITION BY ID
# -------------------------------
def get_petition_by_id(db_path, petition_id):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT petition_text FROM petitions WHERE id = ?", (petition_id,))
    row = cur.fetchone()

    conn.close()
    if row:
        return row[0]
    return "No petition found with that ID."


# -------------------------------
# RUN SAMPLE
# -------------------------------
if __name__ == "__main__":
    db_path = init_database()

    draft = generate_and_store_petition(
        db_path,
        petitioner="Rahul Sharma",
        respondent="Electricity Board",
        court_name="District Civil Court, Kolkata",
        case_type="Electricity Bill Dispute",
        facts_list=[
            "The petitioner received an inflated electricity bill.",
            "Meter reading does not match actual consumption.",
            "Complaints were made but not resolved."
        ],
        reliefs_sought=[
            "Correct the electricity bill",
            "Remove penalty charges",
            "Provide compensation"
        ]
    )

    print("Generated Petition:\n")
    print(draft)

    print("\nStored Petitions (ID, Petitioner, Respondent, Case Type):")
    print(view_all_petitions(db_path))

    print("\nView Petition By ID = 1:\n")
    print(get_petition_by_id(db_path, 1))