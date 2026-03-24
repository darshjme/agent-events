"""Tests for EventHistory."""

import time

import pytest

from agent_events import Event, EventBus, EventHistory


class TestRecord:
    def test_record_increases_size(self):
        h = EventHistory()
        h.record(Event(type="x"))
        assert h.stats()["current_size"] == 1

    def test_ring_buffer_evicts_oldest(self):
        h = EventHistory(max_size=3)
        for i in range(5):
            h.record(Event(type="x", data={"i": i}))
        # Should retain only last 3
        assert h.stats()["current_size"] == 3
        assert h.stats()["total_recorded"] == 5


class TestQuery:
    def test_query_all(self):
        h = EventHistory()
        h.record(Event(type="a"))
        h.record(Event(type="b"))
        results = h.query(limit=10)
        assert len(results) == 2

    def test_query_by_type(self):
        h = EventHistory()
        h.record(Event(type="a"))
        h.record(Event(type="b"))
        h.record(Event(type="a"))
        results = h.query(event_type="a", limit=10)
        assert len(results) == 2
        assert all(e.type == "a" for e in results)

    def test_query_by_source(self):
        h = EventHistory()
        h.record(Event(type="x", source="agent-1"))
        h.record(Event(type="x", source="agent-2"))
        results = h.query(source="agent-1", limit=10)
        assert len(results) == 1
        assert results[0].source == "agent-1"

    def test_query_limit_respected(self):
        h = EventHistory()
        for _ in range(10):
            h.record(Event(type="x"))
        results = h.query(limit=3)
        assert len(results) == 3

    def test_query_combined_filters(self):
        h = EventHistory()
        h.record(Event(type="done", source="agent-1"))
        h.record(Event(type="done", source="agent-2"))
        h.record(Event(type="error", source="agent-1"))
        results = h.query(event_type="done", source="agent-1", limit=10)
        assert len(results) == 1


class TestReplay:
    def test_replay_all(self):
        h = EventHistory()
        bus = EventBus()
        received = []
        bus.subscribe("ping", lambda e: received.append(e))
        h.record(Event(type="ping"))
        h.record(Event(type="ping"))
        replayed = h.replay(bus)
        assert replayed == 2
        assert len(received) == 2

    def test_replay_filtered_by_type(self):
        h = EventHistory()
        bus = EventBus()
        received = []
        bus.subscribe("ping", lambda e: received.append(e))
        h.record(Event(type="ping"))
        h.record(Event(type="pong"))
        replayed = h.replay(bus, event_type="ping")
        assert replayed == 1
        assert len(received) == 1


class TestStats:
    def test_stats_total_recorded(self):
        h = EventHistory(max_size=2)
        h.record(Event(type="x"))
        h.record(Event(type="x"))
        h.record(Event(type="x"))  # evicts first
        assert h.stats()["total_recorded"] == 3

    def test_stats_by_type(self):
        h = EventHistory()
        h.record(Event(type="a"))
        h.record(Event(type="a"))
        h.record(Event(type="b"))
        by_type = h.stats()["by_type"]
        assert by_type["a"] == 2
        assert by_type["b"] == 1

    def test_stats_timestamps(self):
        h = EventHistory()
        e1 = Event(type="x")
        time.sleep(0.01)
        e2 = Event(type="x")
        h.record(e1)
        h.record(e2)
        s = h.stats()
        assert s["oldest_timestamp"] == e1.timestamp
        assert s["newest_timestamp"] == e2.timestamp

    def test_stats_empty_history(self):
        h = EventHistory()
        s = h.stats()
        assert s["total_recorded"] == 0
        assert s["oldest_timestamp"] is None
        assert s["newest_timestamp"] is None
