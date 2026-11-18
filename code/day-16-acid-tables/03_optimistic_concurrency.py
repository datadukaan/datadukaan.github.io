"""Fix 2: optimistic concurrency. Both writers read the same version; the second commit
finds that version taken, re-reads, and decides again: no lost update."""
import shutil, threading, time
from tiny_delta import Table, ConflictError
shutil.rmtree("data/berths", ignore_errors=True)
t = Table("data/berths")
t.commit(-1, add=[t.write_file([{"berth": 72, "passenger": None}])])          # v0: berth 72 free

barrier, log = threading.Barrier(2), []
def book(who, delay):
    while True:
        v = t.latest_version()
        free = t.read(v)[-1]["passenger"] is None
        barrier.wait() if not log else None; time.sleep(delay)
        if not free:
            log.append(f"{who:8s}: read v{v}, berth taken -> WAITING LIST"); return
        new_file = t.write_file([{"berth": 72, "passenger": who}])
        try:
            nv = t.commit(v, add=[new_file], remove=t.files(v))
            log.append(f"{who:8s}: read v{v}, committed v{nv} -> CONFIRMED"); return
        except ConflictError as e:
            log.append(f"{who:8s}: conflict ({e}) -> retry")
threads = [threading.Thread(target=book, args=("Raju", 0.00)), threading.Thread(target=book, args=("stranger", 0.05))]
[x.start() for x in threads]; [x.join() for x in threads]
print("\n".join(log))
print(f"table v{t.latest_version()}: berth 72 -> {t.read()[-1]['passenger']}")
