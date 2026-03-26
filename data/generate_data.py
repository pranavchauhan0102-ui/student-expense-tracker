"""
Generate synthetic student expense dataset for analysis.
Simulates 6 months of daily expenses for 5 students.
"""

import csv
import random
from datetime import date, timedelta

random.seed(42)

STUDENTS = ["Aarav", "Priya", "Rohan", "Sneha", "Vikram"]
CATEGORIES = ["Food", "Transport", "Stationery", "Entertainment", "Utilities", "Medical", "Clothing"]

# Monthly budget per category per student (in INR)
BUDGETS = {
    "Food":          {"mean": 3500, "std": 600},
    "Transport":     {"mean": 1200, "std": 300},
    "Stationery":    {"mean": 600,  "std": 150},
    "Entertainment": {"mean": 800,  "std": 250},
    "Utilities":     {"mean": 500,  "std": 100},
    "Medical":       {"mean": 300,  "std": 200},
    "Clothing":      {"mean": 700,  "std": 400},
}

start_date = date(2024, 7, 1)
end_date   = date(2024, 12, 31)

rows = [["date", "student", "category", "amount"]]

current = start_date
while current <= end_date:
    for student in STUDENTS:
        # Each day, student spends on 1-3 categories
        num_txn = random.randint(1, 3)
        cats = random.sample(CATEGORIES, num_txn)
        for cat in cats:
            b = BUDGETS[cat]
            daily_mean = b["mean"] / 30
            daily_std  = b["std"]  / 30
            amount = max(10, round(random.gauss(daily_mean, daily_std), 2))
            rows.append([current.isoformat(), student, cat, amount])
    current += timedelta(days=1)

with open("expenses.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Generated {len(rows)-1} expense records.")
