"""Move 3: storage tiering. Keep recent data hot; move old partitions you must keep to cheaper tiers.
Prices are approximate list prices per GB-month (AWS S3, us-east-1); check your provider's current pricing."""
PRICE = {"hot (S3 Standard)": 0.023, "cool (S3 Standard-IA)": 0.0125, "archive (Glacier Deep Archive)": 0.00099}
GB_PER_MONTH_OF_DATA = 200          # each month of history is 200 GB
months = list(range(1, 37))         # 3 years kept for compliance

def tier(age_months):
    return "hot (S3 Standard)" if age_months <= 3 else "cool (S3 Standard-IA)" if age_months <= 12 else "archive (Glacier Deep Archive)"

all_hot = len(months) * GB_PER_MONTH_OF_DATA * PRICE["hot (S3 Standard)"]
tiered, by_tier = 0.0, {}
for m in months:
    t = tier(m); by_tier[t] = by_tier.get(t, 0) + GB_PER_MONTH_OF_DATA
    tiered += GB_PER_MONTH_OF_DATA * PRICE[t]
for t, gb in by_tier.items():
    print(f"{t:32s} {gb:>6,} GB  x ${PRICE[t]:.5f} = ${gb*PRICE[t]:>8,.2f}/month")
print(f"\neverything hot : ${all_hot:,.2f}/month")
print(f"tiered         : ${tiered:,.2f}/month  ({all_hot/tiered:.1f}x cheaper)")
print("trade-off      : archive reads take hours and cost extra per GB retrieved")
