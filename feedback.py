import sqlite3
from collections import Counter

DB_PATH = "feedback_memory.db"

def init_feedback_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            notice_text TEXT,
            system_priority TEXT,
            user_priority TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def record_feedback(notice_text, system_priority, user_priority):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO feedback (notice_text, system_priority, user_priority) VALUES (?, ?, ?)",
        (notice_text, system_priority, user_priority)
    )
    conn.commit()
    conn.close()

def compute_corrections():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT system_priority, user_priority FROM feedback")
    rows = cur.fetchall()
    conn.close()

    counts = Counter()
    for sys_p, usr_p in rows:
        if sys_p != usr_p:
            counts[(sys_p, usr_p)] += 1

    learned = {}
    for (sys_p, usr_p), c in counts.items():
        if c >= 2:
            learned[sys_p] = usr_p
    return learned

def adapt_priority(predicted_priority, learned_rules):
    if predicted_priority in learned_rules:
        return learned_rules[predicted_priority]
    return predicted_priority
