from typing import Optional, Dict

from mars.utils import lazy_import
from ..metric import Counter, Gauge, Histogram, Meter, Metric

ray_metrics = lazy_import("ray.util.metrics")


class RayMetric(Metric):
    def _init(self):
        if ray_metrics:
            self._metric = ray_metrics.Gauge(self._name, self._description,
                                             self._tag_keys)

    def _record(self, value=1, tags: Optional[Dict[str, str]] = None):
        if ray_metrics:
            self._metric.record(value, tags)


class CounterImpl(RayMetric, Counter):
    pass


class GaugeImpl(RayMetric, Gauge):
    pass


class MeterImpl(RayMetric, Meter):
    pass


class HistogramImpl(RayMetric, Histogram):
    pass
