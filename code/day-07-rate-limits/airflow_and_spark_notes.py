"""Day 7 - where these fixes live in real tools (not run here).

Airflow: retries with exponential backoff on a task, and a pool to cap how many
tasks hit the same API at once.
"""
# from datetime import timedelta
# from airflow.decorators import task
#
# @task(retries=5, retry_delay=timedelta(seconds=30),
#       retry_exponential_backoff=True, max_retry_delay=timedelta(minutes=10),
#       pool="supplier_api")                         # pool size = how many calls in parallel
# def fetch_prices(page: int): ...

# Python requests: retries with backoff, honouring Retry-After
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# retry = Retry(total=6, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504],
#               respect_retry_after_header=True)
# session.mount("https://", HTTPAdapter(max_retries=retry))

# Spark: don't call an API from thousands of tasks at once.
# Repartition to the number of parallel calls the API allows, then call per partition:
# df.repartition(4).foreachPartition(call_api_with_bucket_and_backoff)

# Azure Data Factory REST source: set the pagination rules (e.g. AbsoluteUrl from
# $.next_page) and "Request interval (ms)" on the copy activity source.
