"""Tiny helper: print a folder tree with file sizes."""
import os
def tree(root, max_files=12):
    shown = 0
    for d, dirs, files in sorted(os.walk(root)):
        dirs.sort()
        rel = os.path.relpath(d, root)
        depth = 0 if rel == "." else rel.count(os.sep) + 1
        if rel != ".":
            print("  " * (depth - 1) + os.path.basename(d) + "/")
        for f in sorted(files):
            if shown >= max_files:
                continue
            shown += 1
            name = f if len(f) <= 44 else f[:20] + "…" + f[-20:]
            print("  " * depth + f"{name}  ({os.path.getsize(os.path.join(d, f)):,} B)")
    if shown >= max_files:
        print("  …")
