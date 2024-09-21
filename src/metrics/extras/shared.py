from dataclasses import dataclass, field
from typing import List, TypeVar
from prometheus_client import Counter, Gauge, Summary, Histogram, Info, Enum

MetricType = TypeVar("MetricType", Counter, Gauge, Summary, Histogram, Info, Enum)


@dataclass(init=True)
class Metric:
    type: str
    name: str
    description: str
    labels: List[str] = field(default_factory=list)
    states: List[str] = field(default_factory=list)


@dataclass(init=True)
class MetricConfig:
    metrics: List[Metric]
    multiproc_dir: str
