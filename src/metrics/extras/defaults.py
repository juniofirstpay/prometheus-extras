from .shared import Metric


defaults = [
    Metric("counter", "http_requests_total", "Counts all the http requests", labels=["method", "endpoint", "status", "version"]),
    Metric("gauge", "http_requests_active", "Tracks all the active http requests", labels=["method", "endpoint", "version"]),
    Metric("histogram", "http_requests_latency", "Counts all http requests latency", labels=["method", "endpoint", "status", "version"])
]