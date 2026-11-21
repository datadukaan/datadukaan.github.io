"""Move 1: VACUUM. Delete files no version within the retention window needs."""
from tiny_delta import Table, vacuum, size_mb
from common import NOW, build
t = build()
before = size_mb(t)
print("dry run   :", len(vacuum(t, NOW, retain_hours=168, dry_run=True)), "files would be deleted")
deleted = vacuum(t, NOW, retain_hours=168)
print(f"VACUUM RETAIN 168 HOURS: deleted {len(deleted)} files, {before:.1f} MB -> {size_mb(t):.1f} MB")
print(f"latest version reads fine : {len(t.read()):,} rows")
v_recent = t.version_as_of("2026-11-16 23:00")
print(f"time travel to 5 days ago (v{v_recent}) : {len(t.read(v_recent)):,} rows")
try:
    t.read(t.version_as_of("2026-10-01 23:00"))
except FileNotFoundError:
    print("time travel to 1 October : FAILED, its files were vacuumed (the trade-off)")
