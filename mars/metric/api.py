import logging
from typing import Dict, Any, Optional, Tuple
from .backends.console import console_metric
from .backends.prometheus import prometheus_metric
from .backends.ray import ray_metric

logger = logging.getLogger(__name__)

_metric_backend = 'console'
_backends_cls = {'console': console_metric,
                 'prometheus': prometheus_metric,
                 'ray': ray_metric}


def init_metrics(config: Dict[str, Any] = {}):
    metric_config = config.get('metric', {}) if config else {}
    global _metric_backend
    _metric_backend = metric_config.get('backend', 'console')
    if _metric_backend not in _backends_cls:
        raise NotImplementedError(
            f'Do not support metric backend {_metric_backend}')
    if _metric_backend == 'prometheus':
        conf = metric_config.get('conf', {})
        port = int(conf.get('port', 0))
        from prometheus_client import start_http_server
        start_http_server(port)
        logger.info('Finished startup prometheus http server and port is %d',
                    port)
    logger.info('Finished initialize the metrics, config is %s, backend is %s',
                config, _metric_backend)


class Metrics:
    """
    A factory to generate different types of metrics.

    Examples
    --------
    >>> c1 = counter('counter1', 'A counter')
    >>> c1.record(1)

    >>> c2 = counter('counter2', 'A counter', ('service', 'tenant'))
    >>> c2.record(1, {'service': 'mars', 'tenant': 'test'})

    >>> g1 = gauge('gauge1')
    >>> g1.record(1)

    >>> m1 = meter('meter1')
    >>> m1.record(1)

    >>> h1 = histogram('histogram1')
    >>> h1.record(1)
    """

    @staticmethod
    def counter(name, description: str = '',
                tag_keys: Optional[Tuple[str]] = None):
        return _backends_cls[_metric_backend].CounterImpl(name,
                                                          description,
                                                          tag_keys)

    @staticmethod
    def gauge(name, description: str = '',
              tag_keys: Optional[Tuple[str]] = None):
        return _backends_cls[_metric_backend].GaugeImpl(name,
                                                        description,
                                                        tag_keys)

    @staticmethod
    def meter(name, description: str = '',
              tag_keys: Optional[Tuple[str]] = None):
        return _backends_cls[_metric_backend].MeterImpl(name,
                                                        description,
                                                        tag_keys)

    @staticmethod
    def histogram(name, description: str = '',
                  tag_keys: Optional[Tuple[str]] = None):
        return _backends_cls[_metric_backend] \
            .HistogramImpl(name,
                           description,
                           tag_keys)
