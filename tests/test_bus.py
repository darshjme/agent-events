"""Tests for EventBus."""

import queue

import pytest

from agent_events import Event, EventBus


# ---------------------------------------------------------------------------
# Subscribe / Unsubscribe
# ---------------------------------------------------------------------------

class TestSubscribeUnsubscribe:
    def test_subscribe_increases_count(self):
        bus = EventBus()
        bus.subscribe("ping", lambda e: None)
        assert bus.subscriber_count("ping") == 1

    def test_duplicate_subscribe_ignored(self):
        bus = EventBus()
        handler = lambda e: None
        bus.subscribe("ping", handler)
        bus.subscribe("ping", handler)
        assert bus.subscriber_count("ping") == 1

    def test_unsubscribe_decreases_count(self):
        bus = EventBus()
        handler = lambda e: None
        bus.subscribe("ping", handler)
        bus.unsubscribe("ping", handler)
        assert bus.subscriber_count("ping") == 0

    def test_unsubscribe_nonexistent_is_noop(self):
        bus = EventBus()
        bus.unsubscribe("ghost", lambda e: None)  # must not raise

    def test_subscriber_count_zero_for_unknown_type(self):
        bus = EventBus()
        assert bus.subscriber_count("unknown") == 0


# ---------------------------------------------------------------------------
# Publish (synchronous)
# ---------------------------------------------------------------------------

class TestPublish:
    def test_publish_calls_handler(self):
        bus = EventBus()
        received = []
        bus.subscribe("ping", lambda e: received.append(e))
        evt = Event(type="ping", data={"msg": "hello"})
        count = bus.publish(evt)
        assert count == 1
        assert received[0] is evt

    def test_publish_returns_handler_count(self):
        bus = EventBus()
        bus.subscribe("x", lambda e: None)
        bus.subscribe("x", lambda e: None, priority=1)
        # Two distinct handlers (lambdas are different objects)
        count = bus.publish(Event(type="x"))
        assert count == 2

    def test_publish_no_subscribers_returns_zero(self):
        bus = EventBus()
        count = bus.publish(Event(type="noop"))
        assert count == 0

    def test_publish_only_matching_type(self):
        bus = EventBus()
        received_a, received_b = [], []
        bus.subscribe("a", lambda e: received_a.append(e))
        bus.subscribe("b", lambda e: received_b.append(e))
        bus.publish(Event(type="a"))
        assert len(received_a) == 1
        assert len(received_b) == 0


# ---------------------------------------------------------------------------
# Priority ordering
# ---------------------------------------------------------------------------

class TestPriority:
    def test_higher_priority_called_first(self):
        bus = EventBus()
        order = []
        bus.subscribe("e", lambda ev: order.append("low"), priority=0)
        bus.subscribe("e", lambda ev: order.append("high"), priority=10)
        bus.publish(Event(type="e"))
        assert order == ["high", "low"]

    def test_equal_priority_preserves_insertion_order(self):
        bus = EventBus()
        order = []
        bus.subscribe("e", lambda ev: order.append(1), priority=5)
        bus.subscribe("e", lambda ev: order.append(2), priority=5)
        bus.publish(Event(type="e"))
        # Both at same priority — insertion order expected
        assert order == [1, 2]


# ---------------------------------------------------------------------------
# Async queue
# ---------------------------------------------------------------------------

class TestAsyncQueue:
    def test_publish_async_does_not_call_handler_immediately(self):
        bus = EventBus()
        called = []
        bus.subscribe("ping", lambda e: called.append(e))
        bus.publish_async(Event(type="ping"))
        assert called == []  # not called yet

    def test_process_queue_dispatches_event(self):
        bus = EventBus()
        called = []
        bus.subscribe("ping", lambda e: called.append(e))
        bus.publish_async(Event(type="ping"))
        bus.process_queue()
        assert len(called) == 1

    def test_process_queue_max_events(self):
        bus = EventBus()
        received = []
        bus.subscribe("x", lambda e: received.append(e))
        for _ in range(10):
            bus.publish_async(Event(type="x"))
        bus.process_queue(max_events=3)
        assert len(received) == 3

    def test_publish_async_raises_when_full(self):
        bus = EventBus(max_queue_size=1)
        bus.publish_async(Event(type="x"))
        with pytest.raises(queue.Full):
            bus.publish_async(Event(type="x"))


# ---------------------------------------------------------------------------
# Clear
# ---------------------------------------------------------------------------

class TestClear:
    def test_clear_specific_type(self):
        bus = EventBus()
        bus.subscribe("a", lambda e: None)
        bus.subscribe("b", lambda e: None)
        bus.clear("a")
        assert bus.subscriber_count("a") == 0
        assert bus.subscriber_count("b") == 1

    def test_clear_all(self):
        bus = EventBus()
        bus.subscribe("a", lambda e: None)
        bus.subscribe("b", lambda e: None)
        bus.clear()
        assert bus.subscriber_count("a") == 0
        assert bus.subscriber_count("b") == 0
