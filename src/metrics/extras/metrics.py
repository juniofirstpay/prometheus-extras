from prometheus_client.multiprocess import MultiProcessCollector
from prometheus_client import (
    CollectorRegistry,
    Counter,
    Gauge,
    Summary,
    Histogram,
    Info,
    Enum,
    generate_latest,
    CONTENT_TYPE_LATEST
)
from typing import Dict, List, Union, Type
from .shared import Metric as MetricConfig, MetricType, MetricConfig as Config


class Metrics:

    _metrics: Dict[str, MetricType]
    _registry: CollectorRegistry

    def __init__(self, config: Config):
        self._registry = CollectorRegistry()

        if config.multiproc_dir:
            MultiProcessCollector(registry=self._registry)

        self._metrics = dict(self._parse(config.metrics))

    async def expose_async(self, scope, receive, send):
        data = generate_latest(self._registry)
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                ('content-type', CONTENT_TYPE_LATEST),
                ('content-length', str(len(data)))
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': data,
        })


    def _parse(self, metrics: List[MetricConfig]):
        _metrics = []
        for metric in metrics:
            metric_cls = self._get_metric_cls(metric.type)
            _metrics.append(
                (metric.name,
                metric_cls(metric.name, metric.description, labelnames=metric.labels)),
            )
        return _metrics

    def _get_metric_cls(self, metric_type: str) -> Type[MetricType]:
        if metric_type == "counter":
            return Counter
        elif metric_type == "gauge":
            return Gauge
        elif metric_type == "summary":
            return Summary
        elif metric_type == "histogram":
            return Histogram
        elif metric_type == "info":
            return Info
        elif metric_type == "enum":
            return Enum

    def _get_metric(self, name: str) -> MetricType:
        metric = self._metrics.get(name, None)
        if metric is None:
            raise NotImplementedError()
        return metric

    def inc(self, name: str, value: Union[int, float] = 1, labels: Dict[str, any] = None):
        metric = self._get_metric(name)
        if not isinstance(metric, (Counter, Gauge)):
            raise TypeError("invalid metric asked for increment")
        if labels is None:
            metric.inc(value)
            return
        metric.labels(**labels).inc(value)

    def dec(
        self, name: str, value: Union[int, float] = 1, labels: Dict[str, any] = None
    ):
        metric = self._get_metric(name)
        if not isinstance(metric, (Counter, Gauge)):
            raise TypeError("invalid metric asked for decrement")

        if labels is None:
            metric.dec(value)
            return
        metric.labels(**labels).dec(value)

    def set(
        self, name: str, value: Union[int, float] = 1, labels: Dict[str, any] = None
    ):
        metric = self._get_metric(name)
        
        if not isinstance(metric, (Counter, Gauge, Summary, Histogram)):
            raise TypeError("invalid metric asked for decrement")

        if isinstance(metric, (Counter, Gauge)):
            if labels is None:
                metric.set(value)
                return
            metric.labels(**labels).set(value)
        elif isinstance(metric, (Summary, Histogram)):
            if labels is None:
                metric.observe(value)
                return
            metric.labels(**labels).observe(value)

    def expose(self) -> bytes:
        return generate_latest(self._registry)
