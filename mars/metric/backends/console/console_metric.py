import logging
from typing import Optional, Dict, Tuple

from ..metric import Counter, Gauge, Histogram, Meter, Metric

logger = logging.getLogger(__name__)


class SimpleMetric:
    def __init__(
        self, name: str, description: str = "", tag_keys: Optional[Tuple[str]] = None
    ):
        self._name = name
        self._description = description
        self._tag_keys = tag_keys
        self._value = None

    def update(self, value: float = 1.0, tags: Optional[Dict[str, str]] = None):
        self._value = value
        logger.debug(
            "Reporting metric with name: %s, description: %s, value: %s, tags: %s",
            self._name,
            self._description,
            value,
            tags,
        )

    @property
    def value(self):
        return self._value


class ConsoleMetric(Metric):
    @property
    def value(self):
        return self._metric.value

    def _init(self):
        self._metric = SimpleMetric(self._name, self._description, self._tag_keys)

    def _record(self, value=1, tags: Optional[Dict[str, str]] = None):
        self._metric.update(value, tags)


class CounterImpl(ConsoleMetric, Counter):
    pass


class GaugeImpl(ConsoleMetric, Gauge):
    pass


class MeterImpl(ConsoleMetric, Meter):
    pass


class HistogramImpl(ConsoleMetric, Histogram):
    pass
