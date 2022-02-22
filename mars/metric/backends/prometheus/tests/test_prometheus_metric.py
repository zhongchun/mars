import time

import pytest
import requests

from ..prometheus_metric import CounterImpl, GaugeImpl, HistogramImpl, MeterImpl

from prometheus_client import start_http_server

_PROMETHEUS_CLIENT_PORT = 49999


@pytest.fixture(scope="module")
def start_prometheus_http_server():
    start_http_server(_PROMETHEUS_CLIENT_PORT)


def verify_metric(name, value, delta=1e-6):
    resp = requests.get("http://127.0.0.1:{}".format(_PROMETHEUS_CLIENT_PORT)).text
    assert name in resp
    lines = resp.splitlines()
    for line in lines:
        if line.startswith(name):
            items = line.split(" ")
            assert len(items) == 2
            assert pytest.approx(float(items[1]), abs=delta) == value


def test_counter(start_prometheus_http_server):
    c = CounterImpl("test_counter", "A test counter", ("service", "tenant"))
    c.record(1, {"service": "mars", "tenant": "test"})
    verify_metric("test_counter", 1.0)
    c.record(2, {"service": "mars", "tenant": "test"})
    verify_metric("test_counter", 3.0)


def test_gauge(start_prometheus_http_server):
    g = GaugeImpl("test_gauge", "A test gauge")
    g.record(0.1)
    verify_metric("test_gauge", 0.1)
    g.record(1.1)
    verify_metric("test_gauge", 1.1)


def test_histogram(start_prometheus_http_server):
    h = HistogramImpl("test_histogram")
    num = 3
    while num > 0:
        h.record(1)
        h.record(2)
        time.sleep(1)
        num -= 1
    verify_metric("test_histogram", 1.5, 0.15)
    num = 3
    while num > 0:
        h.record(3)
        time.sleep(1)
        num -= 1
    # time.sleep(30)
    verify_metric("test_histogram", 3, 0.1)


def test_meter(start_prometheus_http_server):
    m = MeterImpl("test_meter")
    num = 3
    while num > 0:
        m.record(1)
        time.sleep(1)
        num -= 1
    verify_metric("test_meter", 1, 0.05)
