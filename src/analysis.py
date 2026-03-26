"""
Student Expense Tracker - Analysis & Visualization
===================================================
Performs EDA, spending pattern analysis, anomaly detection,
and generates all charts saved to outputs/.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT    = Path(__file__).resolve().parent.parent
DATA    = ROOT / "data" / "expenses.csv"
OUT     = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

PALETTE = ["#4C72B0","#DD8452","#55A868","#C44E52","#8172B2"]
CATS    = ["Food","Transport","Stationery","Entertainment","Utilities","Medical","Clothing"]
CAT_COLORS = {c: col for c, col in zip(CATS,
    ["#e07b54","#4a90d9","#6db56d","#c46e8b","#f0c040","#9b6bb5","#5bbfb5"])}

# ── Load & prep ─────────────────────────────────────────────────────────────
df = pd.read_csv(DATA, parse_dates=["date"])
df["month"]  = df["date"].dt.to_period("M")
df["month_name"] = df["date"].dt.strftime("%b %Y")
df["week"]   = df["date"].dt.isocalendar().week.astype(int)
df["dayofweek"] = df["date"].dt.day_name()

print(f"Loaded {len(df):,} records | {df['student'].nunique()} students | "
      f"{df['date'].min().date()} → {df['date'].max().date()}")

# ── Helper ──────────────────────────────────────────────────────────────────
def save(name):
    path = OUT / name
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path.name}")

# ════════════════════════════════════════════════════════════════════════════
# 1. Monthly spending per student (line chart)
# ════════════════════════════════════════════════════════════════════════════
monthly = (df.groupby(["student","month"])["amount"]
             .sum().reset_index())
monthly["month_dt"] = monthly["month"].dt.to_timestamp()
monthly_pivot = monthly.pivot(index="month_dt", columns="student", values="amount")

fig, ax = plt.subplots(figsize=(10, 5))
for i, col in enumerate(monthly_pivot.columns):
    ax.plot(monthly_pivot.index, monthly_pivot[col],
            marker="o", linewidth=2.2, label=col, color=PALETTE[i])
ax.set_title("Monthly Total Spending per Student", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Month"); ax.set_ylabel("Total Spent (₹)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
ax.legend(title="Student"); ax.grid(alpha=0.3)
plt.tight_layout()
save("01_monthly_spending.png")

# ════════════════════════════════════════════════════════════════════════════
# 2. Category-wise spending breakdown (stacked bar)
# ════════════════════════════════════════════════════════════════════════════
cat_month = (df.groupby(["month","category"])["amount"]
               .sum().unstack(fill_value=0))
cat_month.index = [str(m) for m in cat_month.index]

fig, ax = plt.subplots(figsize=(11, 5))
bottom = np.zeros(len(cat_month))
for cat in CATS:
    if cat in cat_month.columns:
        vals = cat_month[cat].values
        ax.bar(cat_month.index, vals, bottom=bottom,
               label=cat, color=CAT_COLORS[cat], edgecolor="white", linewidth=0.5)
        bottom += vals
ax.set_title("Category-wise Monthly Spending (All Students)", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Month"); ax.set_ylabel("Total Spent (₹)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
ax.legend(loc="upper right", fontsize=8); ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
save("02_category_breakdown.png")

# ════════════════════════════════════════════════════════════════════════════
# 3. Per-student category pie chart (grid)
# ════════════════════════════════════════════════════════════════════════════
students = df["student"].unique()
fig, axes = plt.subplots(1, 5, figsize=(18, 5))
for ax, student in zip(axes, students):
    data = df[df["student"]==student].groupby("category")["amount"].sum()
    colors = [CAT_COLORS.get(c, "#aaaaaa") for c in data.index]
    wedges, texts, autotexts = ax.pie(
        data, autopct="%1.0f%%", colors=colors,
        pctdistance=0.75, startangle=90,
        wedgeprops=dict(edgecolor="white", linewidth=1))
    for t in autotexts: t.set_fontsize(7.5)
    ax.set_title(student, fontsize=11, fontweight="bold")
fig.suptitle("Spending Distribution by Category per Student", fontsize=13, fontweight="bold", y=1.02)
handles = [plt.Rectangle((0,0),1,1, color=CAT_COLORS[c]) for c in CATS]
fig.legend(handles, CATS, loc="lower center", ncol=7, fontsize=8,
           bbox_to_anchor=(0.5, -0.08))
plt.tight_layout()
save("03_student_pies.png")

# ════════════════════════════════════════════════════════════════════════════
# 4. Day-of-week spending heatmap
# ════════════════════════════════════════════════════════════════════════════
DOW_ORDER = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
dow_cat = (df.groupby(["dayofweek","category"])["amount"]
             .mean().unstack(fill_value=0))
dow_cat = dow_cat.reindex(DOW_ORDER)

fig, ax = plt.subplots(figsize=(10, 5))
im = ax.imshow(dow_cat.values, aspect="auto", cmap="YlOrRd")
ax.set_xticks(range(len(dow_cat.columns))); ax.set_xticklabels(dow_cat.columns, rotation=40, ha="right")
ax.set_yticks(range(len(dow_cat.index)));   ax.set_yticklabels(dow_cat.index)
for i in range(len(dow_cat.index)):
    for j in range(len(dow_cat.columns)):
        ax.text(j, i, f"₹{dow_cat.iloc[i,j]:.0f}", ha="center", va="center",
                fontsize=7.5, color="black" if dow_cat.iloc[i,j] < 80 else "white")
plt.colorbar(im, ax=ax, label="Avg Daily Spend (₹)")
ax.set_title("Average Daily Spend by Day of Week & Category", fontsize=13, fontweight="bold", pad=12)
plt.tight_layout()
save("04_heatmap_dow_category.png")

# ════════════════════════════════════════════════════════════════════════════
# 5. Anomaly Detection — Z-score per student per category
# ════════════════════════════════════════════════════════════════════════════
weekly = (df.groupby(["student","week","category"])["amount"]
            .sum().reset_index())
weekly["z"] = (weekly.groupby(["student","category"])["amount"]
                      .transform(lambda x: (x - x.mean()) / (x.std() + 1e-6)))
anomalies = weekly[weekly["z"].abs() > 2.0].copy()
anomalies["flag"] = anomalies["z"].apply(lambda z: "🔺 High" if z > 0 else "🔻 Low")

print(f"\nAnomalies detected: {len(anomalies)}")
print(anomalies[["student","week","category","amount","z","flag"]].head(10).to_string(index=False))

# Plot anomalies per student
fig, ax = plt.subplots(figsize=(10, 5))
anom_count = anomalies.groupby(["student","flag"]).size().unstack(fill_value=0)
colors_anom = {"🔺 High": "#e05c5c", "🔻 Low": "#5c7ee0"}
x = np.arange(len(anom_count.index))
w = 0.35
for i, col in enumerate(anom_count.columns):
    ax.bar(x + (i-0.5)*w, anom_count[col], w, label=col,
           color=colors_anom.get(col,"#aaa"), edgecolor="white")
ax.set_xticks(x); ax.set_xticklabels(anom_count.index)
ax.set_title("Spending Anomalies per Student (Weekly Z-score > 2σ)", fontsize=13, fontweight="bold", pad=12)
ax.set_ylabel("Number of Anomalous Weeks"); ax.legend(); ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
save("05_anomaly_counts.png")

# ════════════════════════════════════════════════════════════════════════════
# 6. Cumulative spending over the semester
# ════════════════════════════════════════════════════════════════════════════
daily_student = (df.groupby(["date","student"])["amount"]
                   .sum().reset_index())
daily_student = daily_student.sort_values("date")
cumulative = (daily_student.groupby(["student","date"])["amount"]
                            .sum()
                            .groupby(level=0).cumsum()
                            .reset_index())
pivot_cum = cumulative.pivot(index="date", columns="student", values="amount")

fig, ax = plt.subplots(figsize=(10, 5))
for i, col in enumerate(pivot_cum.columns):
    ax.plot(pivot_cum.index, pivot_cum[col], linewidth=2.2, label=col, color=PALETTE[i])
ax.set_title("Cumulative Spending Over the Semester", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Date"); ax.set_ylabel("Cumulative Spend (₹)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
ax.legend(title="Student"); ax.grid(alpha=0.3)
plt.tight_layout()
save("06_cumulative_spending.png")

# ════════════════════════════════════════════════════════════════════════════
# 7. Summary stats table
# ════════════════════════════════════════════════════════════════════════════
summary = (df.groupby("student")["amount"]
             .agg(Total="sum", Monthly_Avg=lambda x: x.sum()/6,
                  Daily_Avg="mean", Transactions="count")
             .round(2))
print("\n── Summary Statistics ──")
print(summary.to_string())

summary.to_csv(OUT / "summary_stats.csv")
print("\nAll outputs saved to outputs/")
