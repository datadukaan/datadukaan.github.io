-- Day 16 · ACID table formats: where this lives in your tools (notes, not run)

-- Delta Lake: every write is a commit in _delta_log/; readers see only committed versions
CREATE TABLE bookings (berth INT, passenger STRING, booked_at TIMESTAMP) USING DELTA;
DESCRIBE HISTORY bookings;                          -- one row per committed version
SELECT * FROM bookings VERSION AS OF 7;             -- snapshot / time travel (Day 17)

-- Concurrent writers: optimistic concurrency control. Conflicting commits fail with
-- ConcurrentAppendException / ConcurrentDeleteReadException etc.; retry the job.
-- Reduce conflicts by giving writers disjoint partitions, e.g. WHERE booking_date = '2026-11-18'.
-- Databricks: row-level concurrency (deletion vectors + liquid clustering) lets more writers succeed.

-- Delta isolation levels
ALTER TABLE bookings SET TBLPROPERTIES ('delta.isolationLevel' = 'Serializable');   -- default: WriteSerializable

-- On S3, safe concurrent Delta writes need a commit coordinator (DynamoDB LogStore) or Databricks,
-- because plain S3 has no atomic put-if-absent across writers for older clients.

-- Apache Iceberg: commits swap the table's metadata pointer atomically in the catalog;
-- a writer whose base snapshot is stale gets CommitFailedException and retries.
CALL catalog.system.rollback_to_snapshot('db.bookings', 123456789);

-- Snowflake / warehouses: multi-statement transactions
BEGIN; UPDATE wallet SET balance = balance - 3000 WHERE who = 'Raju';
       INSERT INTO bookings VALUES (72, 'Raju', CURRENT_TIMESTAMP);
COMMIT;
