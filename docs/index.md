---
hide: [navigation, toc]
---

# Data Dukaan

**100 days of data engineering system design, explained like a shop.**

Every app you use, from food delivery to UPI to the shows you're recommended, runs on data pipelines. Each day, Data Dukaan takes **one real problem** data engineers face, tells it as a simple story, and shows **how it's fixed**, with code you can run.

Watch the 60-second videos on [Instagram](https://instagram.com/datadukaan) and [YouTube Shorts](https://youtube.com/@datadukaan). Study the details here.

## Episodes

| Day | Problem | The fixes | |
|---|---|---|---|
| 1 | **Late-arriving data**: why Raju's Sunday sales were wrong | Event time · Watermark · Reprocessing | [Read →](days/day-01-late-arriving-data.md) |

*New day, new problem. The full 100-day plan covers ingestion, storage, batch and streaming, reliability, data quality, modeling, cost, governance and end-to-end designs.*

## Who this is for

- Students exploring data careers
- Engineers switching into data engineering
- Anyone preparing for data engineering interviews
- Anyone curious how apps really work

## Run the code

Every day has runnable examples in [`code/`](https://github.com/datadukaan/datadukaan.github.io/tree/main/code), in PySpark, SQL and dbt, built on a tiny sample dataset so you can see the numbers change on your laptop.

```bash
git clone https://github.com/datadukaan/datadukaan.github.io.git
cd datadukaan.github.io && pip install -r requirements.txt
cd code/day-01-late-arriving-data && python 01_event_time_vs_arrival_time.py
```

*Made by Preetam, a senior data engineer in Mumbai. Examples are generic teaching material and don't reflect any employer's systems.*
