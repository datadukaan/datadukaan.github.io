"""Fix 3: snapshot isolation. A reader pins one version and gets a consistent answer
while a writer is busy creating the next version."""
import shutil
from tiny_delta import Table
shutil.rmtree("data/chart", ignore_errors=True)
t = Table("data/chart")
v = -1
for k in range(8):                                             # versions 0..7: 16 berths booked
    v = t.commit(v, add=[t.write_file([{"berth": k*2 + 1}, {"berth": k*2 + 2}])])
pinned = t.latest_version()
print(f"seat chart pins v{pinned}: {len(t.read(pinned))} berths booked")

new_files = []
for k in range(3):                                             # writer is busy with version 8
    new_files.append(t.write_file([{"berth": 17 + k*2}, {"berth": 18 + k*2}]))
    print(f"  writer wrote {len(new_files)}/3 files for v8 -> chart (v{pinned}) still shows {len(t.read(pinned))}")
v = t.commit(v, add=new_files)
print(f"writer commits v{v}: next refresh shows {len(t.read())} berths, all at once")
print(f"time travel still works: v{pinned} = {len(t.read(pinned))} berths")
