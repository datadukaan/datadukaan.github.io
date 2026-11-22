"""Cold data: 3 years of these files kept for audits. Storage cost by codec.
Price: ~$0.023 per GB-month (S3 Standard list price, approximate)."""
import os
PRICE, DAYS, FILES_PER_DAY = 0.023, 3 * 365, 1000     # a busy table: 1,000 such files a day
for name in ["none", "snappy", "zstd3", "zstd9", "gzip"]:
    gb = os.path.getsize(f"data/orders_{name}.parquet") / 1e9 * DAYS * FILES_PER_DAY
    print(f"{name:7s}: {gb/1000:6.1f} TB -> ${gb*PRICE:>9,.0f}/month")
