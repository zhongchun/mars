import pytest

from mars.metric import init_metrics, api, Metrics


@pytest.fixture
def init():
    init_metrics()


def test_init_metrics():
    init_metrics()
    assert api._metric_backend == 'console'
    init_metrics({'metric': {}})
    assert api._metric_backend == 'console'
    init_metrics({'metric': {'backend': 'console'}})
    assert api._metric_backend == 'console'
    init_metrics({'metric': {'backend': 'ray'}})
    assert api._metric_backend == 'ray'
    init_metrics({'metric': {'backend': 'prometheus'}})
    assert api._metric_backend == 'prometheus'
    with pytest.raises(NotImplementedError):
        init_metrics({'metric': {'backend': 'not_exist'}})


def test_counter(init):
    c = Metrics.counter('test_counter', 'A test counter', ("service", "tenant"))
    c.record(1, {"service": "mars", "tenant": "test"})
    c.record(2, {"service": "mars", "tenant": "test"})
    assert c.name == "test_counter"
    assert c.tag_keys == ("service", "tenant")
    assert c.value == 3


def test_gauge():
    g = Metrics.gauge('test_gauge', "A test gauge")
    g.record(1)
    assert g.name == "test_gauge"
    assert g.tag_keys == ()
    assert g.value == 1


def test_meter():
    m = Metrics.meter('test_meter')
    m.record(1)
    assert m.name == "test_meter"
    assert m.tag_keys == ()


def test_histogram():
    h = Metrics.histogram('test_histogram')
    h.record(1)
    assert h.name == "test_histogram"
    assert h.tag_keys == ()
