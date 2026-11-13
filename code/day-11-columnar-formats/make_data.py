"""Raju's register: 1,000,000 bills (Jan 2025 - Nov 2026), saved as CSV (row by row)."""
import csv, os, random, datetime as dt
random.seed(11)
ITEMS = [("samosa", 20), ("chai", 15), ("rice", 90), ("dal", 110), ("oil", 180), ("sugar", 45), ("soap", 40), ("biscuit", 30)]
CUST = ["Amit", "Neha", "Ravi", "Sita", "Joy", "Anu", "Imran", "Priya", "Karan", "Meera"]
N = 1_000_000
start = dt.date(2025, 1, 1); days = (dt.date(2026, 11, 30) - start).days
os.makedirs("data", exist_ok=True)
with open("data/bills.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["bill_date", "customer", "item", "qty", "price", "tax"])
    for i in range(N):                      # bills are written in date order, like a real register
        d = start + dt.timedelta(days=i * days // N)
        item, p = random.choice(ITEMS) if random.random() > 0.4 else ITEMS[0]   # samosa is the bestseller
        q = random.randint(1, 5); price = p * q
        w.writerow([d.isoformat(), random.choice(CUST), item, q, price, round(price * 0.05, 2)])
print(f"data/bills.csv: {N:,} bills, {os.path.getsize('data/bills.csv')/1e6:.1f} MB")
