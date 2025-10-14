# db_check.py
import sqlite3

DB = "reminders.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

print("Reminders:")
for row in cur.execute("SELECT id, chat_id, time, label, active FROM reminders"):
    print(row)

print("\nConfirmations:")
for row in cur.execute("SELECT id, reminder_id, chat_id, ts, note FROM confirmations"):
    print(row)

conn.close()
