from ..console_metric import CounterImpl, GaugeImpl, MeterImpl, HistogramImpl


def test_counter():
    c = CounterImpl('test_counter', 'A test counter', ("service", "tenant"))
    c.record(1, {"service": "mars", "tenant": "test"})
    c.record(2, {"service": "mars", "tenant": "test"})
    assert c.name == "test_counter"
    assert c.tag_keys == ("service", "tenant")
    assert c.value == 3


def test_gauge():
    g = GaugeImpl('test_gauge', "A test gauge")
    g.record(1)
    assert g.name == "test_gauge"
    assert g.tag_keys == ()
    assert g.value == 1


def test_meter():
    m = MeterImpl('test_meter')
    m.record(1)
    assert m.name == "test_meter"
    assert m.tag_keys == ()


def test_histogram():
    h = HistogramImpl('test_histogram')
    h.record(1)
    assert h.name == "test_histogram"
    assert h.tag_keys == ()
