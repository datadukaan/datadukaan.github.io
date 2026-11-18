"""A tiny Delta-style table, ~60 lines, to show how ACID table formats work.

Layout (same idea as Delta Lake):
    table/
      part-<uuid>.parquet          data files (written first, invisible on their own)
      _delta_log/00000000.json     commit 0: files added / removed
      _delta_log/00000001.json     commit 1 ...
A version exists only when its log file exists. Creating that file is atomic and
"put-if-absent" (O_EXCL), so two writers can't both create the same version.
"""
import json, os, uuid
import pyarrow as pa, pyarrow.parquet as pq

class ConflictError(Exception):
    pass

class Table:
    def __init__(self, path):
        self.path, self.log = path, os.path.join(path, "_delta_log")
        os.makedirs(self.log, exist_ok=True)

    def latest_version(self):
        vs = [int(n.split(".")[0]) for n in os.listdir(self.log) if n.endswith(".json")]
        return max(vs) if vs else -1

    def files(self, version=None):
        """Replay the log up to `version`: the snapshot is the set of live files."""
        version = self.latest_version() if version is None else version
        live = set()
        for v in range(version + 1):
            entry = json.load(open(os.path.join(self.log, f"{v:08d}.json")))
            live |= set(entry["add"]); live -= set(entry["remove"])
        return sorted(live)

    def read(self, version=None):
        fs = self.files(version)
        return pa.concat_tables(pq.read_table(os.path.join(self.path, f)) for f in fs).to_pylist() if fs else []

    def write_file(self, rows):
        """Step 1: write a data file. Nobody can see it yet."""
        name = f"part-{uuid.uuid4().hex[:8]}.parquet"
        pq.write_table(pa.Table.from_pylist(rows), os.path.join(self.path, name))
        return name

    def commit(self, read_version, add, remove=()):
        """Step 2: one atomic, put-if-absent log entry makes the files real."""
        new = read_version + 1
        try:
            fd = os.open(os.path.join(self.log, f"{new:08d}.json"), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise ConflictError(f"version {new} already exists: someone committed after you read v{read_version}")
        with os.fdopen(fd, "w") as f:
            json.dump({"add": list(add), "remove": list(remove)}, f)
        return new
