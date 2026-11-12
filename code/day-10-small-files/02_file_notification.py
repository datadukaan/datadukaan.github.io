"""Fix 1: the storage tells us when a file lands (a queue of events), so no folder polling."""
import os, queue, threading, time
from common import fresh

LANDING = "landing"
fresh(LANDING)
events = queue.Queue()                     # stands in for Event Grid / SQS / Pub/Sub

def storage_upload(name, body):
    """Upload a file, then the storage service publishes a 'file landed' event."""
    path = os.path.join(LANDING, name)
    with open(path, "w") as f:
        f.write(body)
    events.put({"event": "ObjectCreated", "path": path})

def supplier():
    for i in range(10):
        storage_upload(f"order_{i:05d}.json", '{"amount": 40}')
        time.sleep(0.05)
    events.put(None)                         # end of demo

threading.Thread(target=supplier).start()
got = 0
while (e := events.get()) is not None:      # blocks quietly, no LIST calls
    got += 1
print(f"files received via events: {got}")
print("folder LIST calls        : 0")
