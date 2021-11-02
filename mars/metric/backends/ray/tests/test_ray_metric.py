from mars.tests.core import require_ray
from ..ray_metric import CounterImpl, GaugeImpl, HistogramImpl, MeterImpl


@require_ray
def test_counter():
    c = CounterImpl('test_counter', "A test counter", ("service", "tenant"))
    c.record(1, {"service": "mars", "tenant": "test"})
    assert c.name == "test_counter"
    assert c.tag_keys == ("service", "tenant")


@require_ray
def test_gauge():
    g = GaugeImpl('test_gauge', "A test gauge")
    g.record(1)
    assert g.name == "test_gauge"
    assert g.tag_keys == ()


@require_ray
def test_meter():
    m = MeterImpl('test_meter')
    m.record(1)
    assert m.name == "test_meter"
    assert m.tag_keys == ()


@require_ray
def test_histogram():
    h = HistogramImpl('test_histogram')
    h.record(1)
    assert h.name == "test_histogram"
    assert h.tag_keys == ()
