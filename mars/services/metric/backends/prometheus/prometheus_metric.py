from typing import Optional, Dict
from prometheus_client import Gauge as PGauge

from ..metric import Counter, Gauge, Histogram, Meter, Metric


class PrometheusMetric(Metric):
    def _init(self):
        self._metric = PGauge(self._name, self._description, self._tag_keys)

    def _record(self, value=1, tags: Optional[Dict[str, str]] = None):
        if tags:
            self._metric.labels(**tags).set(value)
        else:
            self._metric.set(value)


class CounterImpl(PrometheusMetric, Counter):
    pass


class GaugeImpl(PrometheusMetric, Gauge):
    pass


class MeterImpl(PrometheusMetric, Meter):
    pass


class HistogramImpl(PrometheusMetric, Histogram):
    pass
