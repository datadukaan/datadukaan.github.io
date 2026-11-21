"""Day 16's tiny Delta-style table, plus what Day 17 needs: commit info (who/when/what),
history, time travel by version or timestamp, and restore.

    table/part-*.parquet          data files (never modified, never deleted by a commit)
    table/_delta_log/00000000.json  {"add": [...], "remove": [...], "commitInfo": {...}}
Because a commit only *adds* a log entry and old data files stay on disk,
every earlier version can still be rebuilt by replaying the log up to it.
"""
import json, os, uuid
import pyarrow as pa, pyarrow.parquet as pq

class Table:
    def __init__(self, path):
        self.path, self.log = path, os.path.join(path, "_delta_log")
        os.makedirs(self.log, exist_ok=True)

    def _entry(self, v):
        return json.load(open(os.path.join(self.log, f"{v:08d}.json")))

    def latest_version(self):
        vs = [int(n.split(".")[0]) for n in os.listdir(self.log) if n.endswith(".json")]
        return max(vs) if vs else -1

    def files(self, version=None):
        version = self.latest_version() if version is None else version
        live = set()
        for v in range(version + 1):
            e = self._entry(v); live |= set(e["add"]); live -= set(e["remove"])
        return sorted(live)

    def read(self, version=None):
        fs = self.files(version)
        return pa.concat_tables(pq.read_table(os.path.join(self.path, f)) for f in fs).to_pylist() if fs else []

    def commit(self, rows, operation, user, timestamp, mode="overwrite"):
        """Write new data; 'overwrite' logically removes the old files (they stay on disk)."""
        name = f"part-{uuid.uuid4().hex[:8]}.parquet"
        pq.write_table(pa.Table.from_pylist(rows), os.path.join(self.path, name))
        v = self.latest_version()
        remove = self.files(v) if (mode == "overwrite" and v >= 0) else []
        return self._log(v + 1, [name], remove, operation, user, timestamp)

    def _log(self, new, add, remove, operation, user, timestamp, **extra):
        fd = os.open(os.path.join(self.log, f"{new:08d}.json"), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w") as f:
            json.dump({"add": add, "remove": remove,
                       "commitInfo": {"operation": operation, "user": user, "timestamp": timestamp, **extra}}, f)
        return new

    # --- Fix 1: history ---
    def history(self):
        return [{"version": v, **self._entry(v)["commitInfo"]} for v in range(self.latest_version(), -1, -1)]

    # --- Fix 2: time travel ---
    def version_as_of(self, timestamp):
        """Latest version committed at or before `timestamp`."""
        ok = [h["version"] for h in self.history() if h["timestamp"] <= timestamp]
        if not ok: raise ValueError(f"no version at or before {timestamp}")
        return max(ok)

    # --- Fix 3: restore ---
    def restore(self, version, user, timestamp):
        """A new commit whose live files equal those of `version`. History is kept."""
        cur, target = set(self.files()), set(self.files(version))
        return self._log(self.latest_version() + 1, sorted(target - cur), sorted(cur - target),
                         "RESTORE", user, timestamp, restoredVersion=version)


# --- Day 18: VACUUM ---------------------------------------------------------
from datetime import datetime, timedelta

def _ts(s): return datetime.strptime(s, "%Y-%m-%d %H:%M")

def vacuum(table, now, retain_hours=168, dry_run=False):
    """Delete data files that are not live now AND were removed from the table more
    than `retain_hours` ago. Versions older than that can no longer be time-travelled."""
    live = set(table.files())
    removed_at = {}
    for h in table.history():                       # newest first
        e = table._entry(h["version"])
        for f in e["remove"]:
            removed_at.setdefault(f, _ts(h["timestamp"]))
    cutoff = _ts(now) - timedelta(hours=retain_hours)
    on_disk = [f for f in os.listdir(table.path) if f.endswith(".parquet")]
    doomed = [f for f in on_disk if f not in live and removed_at.get(f, _ts(now)) < cutoff]
    if not dry_run:
        for f in doomed: os.remove(os.path.join(table.path, f))
    return doomed

def size_mb(table):
    return sum(os.path.getsize(os.path.join(table.path, f)) for f in os.listdir(table.path) if f.endswith(".parquet")) / 1e6
