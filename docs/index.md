---
hide: [navigation, toc]
title: Data engineering, explained like a shop
---

<div class="dd-hero" markdown>
<div class="dd-hero-text" markdown>
<span class="dd-eyebrow">100-day challenge · Day 1 is live</span>

# Data engineering,<br><span class="dd-amber">explained like a shop.</span>

Every app you use, from food delivery to UPI to the shows you're recommended, runs on data pipelines. Each day, **one real problem** data engineers face, told as a simple story, with the fix and **code you can run**.

<div class="dd-buttons" markdown>
[Start with Day 1 →](days/day-01-late-arriving-data.md){ .md-button .md-button--primary }
[Watch on Instagram](https://instagram.com/datadukaan){ .md-button }
</div>
</div>
<div class="dd-hero-art"><img src="assets/logo.png" alt="Data Dukaan logo: a shop awning over rising sales bars"></div>
</div>

<div class="dd-progress" markdown>
<div class="dd-progress-bar"><span style="width:11%"></span></div>
<p><strong>11</strong> of 100 days published · new problem every day</p>
</div>

## How it works

<div class="dd-grid3" markdown>
<div class="dd-card" markdown>
<span class="dd-num">1</span>
### Watch 60 seconds
A short story on Instagram or YouTube Shorts. No jargon, just a shop, a notebook and a problem.
</div>
<div class="dd-card" markdown>
<span class="dd-num">2</span>
### Read the real version
The same problem in proper data engineering terms: why it happens, each fix, trade-offs and interview questions.
</div>
<div class="dd-card" markdown>
<span class="dd-num">3</span>
### Run the code
PySpark, SQL and dbt examples on a tiny sample dataset. Watch the numbers change on your own laptop.
</div>
</div>

## Episodes

<div class="dd-episodes" markdown>
<a class="dd-ep" href="days/day-01-late-arriving-data/">
  <span class="dd-ep-day">DAY 1</span>
  <span class="dd-ep-title">Why Raju's sales were wrong</span>
  <span class="dd-ep-sub">Late-arriving data</span>
  <span class="dd-tags"><span>event time</span><span>watermark</span><span>reprocessing</span></span>
</a>
<a class="dd-ep" href="days/day-02-duplicate-data/">
  <span class="dd-ep-day">DAY 2</span>
  <span class="dd-ep-title">Why Raju's sales were too high</span>
  <span class="dd-ep-sub">Duplicate data</span>
  <span class="dd-tags"><span>unique ID</span><span>deduplication</span><span>idempotent write</span></span>
</a>
<a class="dd-ep" href="days/day-03-out-of-order-data/">
  <span class="dd-ep-day">DAY 3</span>
  <span class="dd-ep-title">Why Raju lost ₹300 on one order</span>
  <span class="dd-ep-sub">Out-of-order data</span>
  <span class="dd-tags"><span>event time</span><span>sequence number</span><span>latest version wins</span></span>
</a>
<a class="dd-ep" href="days/day-04-incremental-loads/">
  <span class="dd-ep-day">DAY 4</span>
  <span class="dd-ep-title">Why Raju's shop opened late</span>
  <span class="dd-ep-sub">Incremental loads</span>
  <span class="dd-tags"><span>high-water mark</span><span>incremental load</span><span>lookback window</span></span>
</a>
<a class="dd-ep" href="days/day-05-change-data-capture/">
  <span class="dd-ep-day">DAY 5</span>
  <span class="dd-ep-title">Why Raju lost ₹1,200 on one price</span>
  <span class="dd-ep-sub">Change Data Capture</span>
  <span class="dd-tags"><span>change log</span><span>CDC</span><span>checkpoint</span></span>
</a>
<a class="dd-ep" href="days/day-06-soft-deletes/">
  <span class="dd-ep-day">DAY 6</span>
  <span class="dd-ep-title">Why Raju paid tax on a cancelled order</span>
  <span class="dd-ep-sub">Soft deletes &amp; tombstones</span>
  <span class="dd-tags"><span>soft delete</span><span>tombstone</span><span>filtered view</span></span>
</a>
<a class="dd-ep" href="days/day-07-rate-limits/">
  <span class="dd-ep-day">DAY 7</span>
  <span class="dd-ep-title">Why Raju lost a ₹50,000 order</span>
  <span class="dd-ep-sub">Rate limits &amp; backoff</span>
  <span class="dd-tags"><span>rate limit</span><span>exponential backoff</span><span>pagination</span></span>
</a>
<a class="dd-ep" href="days/day-08-partial-reads/">
  <span class="dd-ep-day">DAY 8</span>
  <span class="dd-ep-title">Why the Diwali boxes were empty</span>
  <span class="dd-ep-sub">Partial reads</span>
  <span class="dd-tags"><span>atomic rename</span><span>_SUCCESS</span><span>manifest</span></span>
</a>
<a class="dd-ep" href="days/day-09-schema-evolution/">
  <span class="dd-ep-day">DAY 9</span>
  <span class="dd-ep-title">Why Raju paid ₹1,800, not ₹18,000</span>
  <span class="dd-ep-sub">Schema drift</span>
  <span class="dd-tags"><span>read by name</span><span>schema evolution</span><span>data contract</span></span>
</a>
<a class="dd-ep" href="days/day-10-small-files/">
  <span class="dd-ep-day">DAY 10</span>
  <span class="dd-ep-title">Why Raju's son ran 2,000 times</span>
  <span class="dd-ep-sub">The small files problem</span>
  <span class="dd-tags"><span>file notification</span><span>micro-batching</span><span>batch trigger</span></span>
</a>
<a class="dd-ep" href="days/day-11-columnar-formats/">
  <span class="dd-ep-day">DAY 11</span>
  <span class="dd-ep-title">Why Raju read 10,000 bills for 1 column</span>
  <span class="dd-ep-sub">Columnar formats</span>
  <span class="dd-tags"><span>Parquet</span><span>compression</span><span>predicate pushdown</span></span>
</a>
<div class="dd-ep dd-ep-soon">
  <span class="dd-ep-day">DAY 12</span>
  <span class="dd-ep-title">coming soon</span>
  <span class="dd-ep-sub">Module 2 · Storing data</span>
</div>
</div>

## The 100-day path

<div class="dd-modules">
  <div><b>1–10</b> How data arrives</div>
  <div><b>11–20</b> Storing data</div>
  <div><b>21–30</b> Big batch processing</div>
  <div><b>31–40</b> Real-time streaming</div>
  <div><b>41–50</b> Scheduling &amp; reliability</div>
  <div><b>51–60</b> Data quality &amp; trust</div>
  <div><b>61–70</b> Data modeling</div>
  <div><b>71–80</b> Speed &amp; cost</div>
  <div><b>81–90</b> Security &amp; governance</div>
  <div><b>91–100</b> End-to-end designs</div>
</div>

## Who it's for

<div class="dd-grid4">
  <div class="dd-chip-card">🎓 Students exploring data careers</div>
  <div class="dd-chip-card">🔁 Career switchers</div>
  <div class="dd-chip-card">🎯 Interview preparation</div>
  <div class="dd-chip-card">💡 Anyone curious how apps work</div>
</div>

<div class="dd-about" markdown>
**Made by Preetam**, a senior data engineer in Mumbai with 5+ years of building data pipelines for large financial companies.
Follow along on [Instagram](https://instagram.com/datadukaan) and [YouTube](https://youtube.com/@datadukaan). All code is on [GitHub](https://github.com/datadukaan/datadukaan.github.io).
<br><small>Examples are generic teaching material and don't reflect any employer's systems.</small>
</div>
