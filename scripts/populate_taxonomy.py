import sqlite3
from pathlib import Path

# Path to your taxonomy.sqlite
db_path = Path("mcp_servers/taxonomy_server/data/taxonomy.sqlite")
db_path.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists

# Connect (creates file if not exists)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS taxonomy (
    category TEXT PRIMARY KEY,
    description TEXT
)
""")

# Insert taxonomy categories
categories = [
    ("finance.invoice", "Documents related to invoices, payments, and bills."),
    ("finance.expense_report", "Internal employee expense reports."),
    ("hr.leave_request", "Requests for leave or time off."),
    ("hr.policy", "Internal HR policies and guidelines."),
    ("legal.contract", "Contracts, agreements, and legal documents.")
]

cursor.executemany("INSERT OR REPLACE INTO taxonomy (category, description) VALUES (?, ?)", categories)

conn.commit()
conn.close()

print(f"taxonomy.sqlite populated with {len(categories)} categories at {db_path}")
