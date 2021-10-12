from typing import Dict
from ..core import AbstractService
from .backends.console import console_metric
from .backends.prometheus import prometheus_metric
from .backends.ray import ray_metric


class Metrics:
    """
    A factory to generate different types of metrics.

    Examples
    --------
    >>> c1 = Metrics.counter('counter1', 'A counter')
    >>> c1.record(1)

    >>> c2 = Metrics.counter('counter2', 'A counter', ('service', 'tenant'))
    >>> c2.record(1, {'service': 'mars', 'tenant': 'test'})

    >>> g1 = Metrics.gauge('gauge1')
    >>> g1.record(1)

    >>> m1 = Metrics.meter('meter1')
    >>> m1.record(1)

    >>> h1 = Metrics.histogram('histogram1')
    >>> h1.record(1)
    """
    _backend = 'console'
    _backends_cls = {'console': console_metric,
                     'prometheus': prometheus_metric,
                     'ray': ray_metric}

    def __init__(self, config: Dict[str, str]):
        metric_config = config.get('metric', {}) if config else {}
        self._backend = metric_config.get('backend', 'console')
        if self._backend == 'prometheus':
            conf = metric_config.get('conf', {})
            # 0 indicates a random port
            port = int(conf.get('port', 0))
            from prometheus_client import start_http_server
            start_http_server(port)

    @staticmethod
    def counter(name, description, tag_keys):
        return Metrics._backends_cls[Metrics._backend].CounterImpl(name,
                                                                   description,
                                                                   tag_keys)

    @staticmethod
    def gauge(name, description, tag_keys):
        return Metrics._backends_cls[Metrics._backend].GaugeImpl(name,
                                                                 description,
                                                                 tag_keys)

    @staticmethod
    def meter(name, description, tag_keys):
        return Metrics._backends_cls[Metrics._backend].MeterImpl(name,
                                                                 description,
                                                                 tag_keys)

    @staticmethod
    def histogram(name, description, tag_keys):
        return Metrics._backends_cls[Metrics._backend] \
            .HistogramImpl(name,
                           description,
                           tag_keys)


class MetricCommonService(AbstractService):
    """
    Metric common service

    Service Configuration
    ---------------------
    {
        "metric": {
            "backend": "<metric backend name>"
            "conf": {
            }
        }
    }
    """

    async def start(self):
        Metrics(self._config)

    async def stop(self):
        pass
