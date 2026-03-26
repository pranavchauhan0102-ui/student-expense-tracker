# 💸 Student Expense Tracker & Spending Pattern Analyzer

A data science project that analyzes student spending behavior across categories over a semester, detects anomalous spending weeks, and generates rich visualizations to help students understand their financial habits.

---

## 📌 Problem Statement

Students often struggle to understand where their money goes each month. Unlike working professionals, students have tight, fixed budgets — yet most lack visibility into their own spending patterns. This project simulates and analyzes 6 months of expense data for 5 students, uncovering category-wise trends, day-of-week habits, and anomalous spending spikes using exploratory data analysis (EDA) and statistical anomaly detection.

---

## 🗂️ Project Structure

```
student-expense-tracker/
├── data/
│   ├── generate_data.py       # Synthetic data generator
│   └── expenses.csv           # Generated dataset (1,816 records)
├── src/
│   └── analysis.py            # Main EDA + visualization + anomaly detection
├── outputs/
│   ├── 01_monthly_spending.png
│   ├── 02_category_breakdown.png
│   ├── 03_student_pies.png
│   ├── 04_heatmap_dow_category.png
│   ├── 05_anomaly_counts.png
│   ├── 06_cumulative_spending.png
│   └── summary_stats.csv
├── requirements.txt
└── README.md
```

---

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip

### 1. Clone the repository
```bash
git clone https://github.com/pranavchauhan0102-ui/student-expense-tracker.git
cd student-expense-tracker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate the dataset
```bash
python data/generate_data.py
```
This creates `data/expenses.csv` with 1,816+ simulated expense records across 5 students, 7 categories, and 6 months.

### 4. Run the analysis
```bash
python src/analysis.py
```
All charts and the summary CSV are saved to the `outputs/` folder.

---

## 📊 What It Analyzes

| Analysis | Description |
|---|---|
| Monthly spending trends | Line chart showing how each student's total spend changed over 6 months |
| Category breakdown | Stacked bar chart of where money goes each month |
| Per-student distribution | Pie charts showing each student's spending mix |
| Day-of-week heatmap | Which days & categories see the highest average spend |
| Anomaly detection | Weekly Z-score flagging of unusually high or low spending |
| Cumulative spend | Running total across the semester per student |

---

## 🧠 Key Techniques Used

- **Pandas** — data loading, groupby aggregations, pivot tables
- **Matplotlib** — all visualizations (line, bar, pie, heatmap)
- **NumPy** — Z-score computation for anomaly detection
- **Statistical Analysis** — mean, standard deviation, Z-score thresholding (|Z| > 2σ)

---

## 📦 Requirements

```
pandas
matplotlib
numpy
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 📈 Sample Output

After running `analysis.py`, you'll find 6 charts in `outputs/`:

- **Monthly Spending** — see who spends the most and how it changes month to month
- **Category Heatmap** — discover high-spend days (e.g., weekends spike in Entertainment & Food)
- **Anomaly Report** — 29 anomalous weeks detected across 5 students

---

## 🔍 Dataset Details

| Field | Description |
|---|---|
| `date` | Date of transaction (2024-07-01 to 2024-12-31) |
| `student` | Student name (Aarav, Priya, Rohan, Sneha, Vikram) |
| `category` | Expense category (Food, Transport, Stationery, Entertainment, Utilities, Medical, Clothing) |
| `amount` | Transaction amount in INR (₹) |

Data is synthetically generated using realistic Indian student budget distributions with Gaussian noise.

---

## 💡 Insights Found

- **Food** consistently accounts for the largest share of spending (~35–40%) across all students
- **Weekends** show elevated Entertainment and Food spending, visible in the heatmap
- **Aarav** had the highest total semester spend (₹14,855) while **Rohan** was the most frugal (₹12,036)
- **29 anomalous weeks** were detected — mostly high-spend spikes in Food and Transport

---

## 👤 Author

Made as part of a Data Science course BYOP (Bring Your Own Project) submission.
