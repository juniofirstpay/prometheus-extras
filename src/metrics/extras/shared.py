from dataclasses import dataclass
from typing import List, TypeVar
from prometheus_client import Counter, Gauge, Summary, Histogram, Info, Enum

MetricType = TypeVar("MetricType", Counter, Gauge, Summary, Histogram, Info, Enum)


@dataclass(init=True)
class Metric:
    type: str
    name: str
    description: str
    labels: List[str] = []
    states: List[str] = []


@dataclass(init=True)
class MetricConfig:
    metrics: List[Metric]
    multiproc_dir: str
