"""Move 2: a retention policy per table, applied by one job instead of ad hoc."""
POLICY = {   # table        keep versions for    keep rows for            why
    "tax_invoices":  {"time_travel_days": 30, "row_retention": "8 years", "reason": "tax law"},
    "sales":         {"time_travel_days": 7,  "row_retention": "3 years", "reason": "reporting"},
    "clickstream":   {"time_travel_days": 7,  "row_retention": "90 days", "reason": "analytics only"},
    "tmp_staging":   {"time_travel_days": 1,  "row_retention": "7 days",  "reason": "scratch"},
}
print(f"{'table':14s} {'VACUUM RETAIN':>14s}   {'delete rows older than':22s} reason")
for name, p in POLICY.items():
    print(f"{name:14s} {p['time_travel_days']*24:>10d} HOURS   {p['row_retention']:22s} {p['reason']}")
print("\nGenerated maintenance SQL:")
for name, p in POLICY.items():
    print(f"ALTER TABLE {name} SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval {p['time_travel_days']} days');")
    print(f"VACUUM {name};")
