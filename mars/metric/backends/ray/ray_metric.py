from typing import Optional, Dict

from mars.utils import lazy_import
from ..metric import Counter, Gauge, Histogram, Meter, Metric

ray_metrics = lazy_import("ray.util.metrics")

# Note: Gauge record method will be deprecated in new ray version, so here
# make it compatible with the old and new ray version.
RAY_GAUGE_SET_AVAILABLE = True if ray_metrics and hasattr(ray_metrics.Gauge,
                                                          'set') else False


class RayMetric(Metric):
    def _init(self):
        if ray_metrics:
            self._metric = ray_metrics.Gauge(self._name, self._description,
                                             self._tag_keys)

    def _record(self, value=1, tags: Optional[Dict[str, str]] = None):
        if RAY_GAUGE_SET_AVAILABLE:
            self._metric.set(value, tags)
        elif ray_metrics:
            self._metric.record(value, tags)


class CounterImpl(RayMetric, Counter):
    pass


class GaugeImpl(RayMetric, Gauge):
    pass


class MeterImpl(RayMetric, Meter):
    pass


class HistogramImpl(RayMetric, Histogram):
    pass
