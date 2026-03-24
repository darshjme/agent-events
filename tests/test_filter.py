"""Tests for EventFilter."""

import pytest

from agent_events import Event, EventBus, EventFilter


class TestSourceFilter:
    def test_matching_source_calls_handler(self):
        bus = EventBus()
        received = []

        @EventFilter.where(source="agent-1")
        def handler(evt: Event):
            received.append(evt)

        bus.subscribe("done", handler)
        evt = Event(type="done", source="agent-1")
        bus.publish(evt)
        assert len(received) == 1

    def test_non_matching_source_skips_handler(self):
        bus = EventBus()
        received = []

        @EventFilter.where(source="agent-1")
        def handler(evt: Event):
            received.append(evt)

        bus.subscribe("done", handler)
        bus.publish(Event(type="done", source="agent-2"))
        assert received == []


class TestDataContainsFilter:
    def test_matching_data_calls_handler(self):
        bus = EventBus()
        received = []

        @EventFilter.where(data_contains={"status": "done"})
        def handler(evt: Event):
            received.append(evt)

        bus.subscribe("task", handler)
        bus.publish(Event(type="task", data={"status": "done", "extra": True}))
        assert len(received) == 1

    def test_non_matching_data_skips_handler(self):
        bus = EventBus()
        received = []

        @EventFilter.where(data_contains={"status": "done"})
        def handler(evt: Event):
            received.append(evt)

        bus.subscribe("task", handler)
        bus.publish(Event(type="task", data={"status": "running"}))
        assert received == []

    def test_missing_key_skips_handler(self):
        bus = EventBus()
        received = []

        @EventFilter.where(data_contains={"status": "done"})
        def handler(evt: Event):
            received.append(evt)

        bus.subscribe("task", handler)
        bus.publish(Event(type="task", data={}))
        assert received == []


class TestMinPriorityFilter:
    def test_sufficient_priority_calls_handler(self):
        bus = EventBus()
        received = []

        @EventFilter.where(min_priority=5)
        def handler(evt: Event):
            received.append(evt)

        bus.subscribe("alert", handler)
        bus.publish(Event(type="alert", data={"priority": 7}))
        assert len(received) == 1

    def test_insufficient_priority_skips_handler(self):
        bus = EventBus()
        received = []

        @EventFilter.where(min_priority=5)
        def handler(evt: Event):
            received.append(evt)

        bus.subscribe("alert", handler)
        bus.publish(Event(type="alert", data={"priority": 3}))
        assert received == []

    def test_missing_priority_field_skips_handler(self):
        bus = EventBus()
        received = []

        @EventFilter.where(min_priority=5)
        def handler(evt: Event):
            received.append(evt)

        bus.subscribe("alert", handler)
        bus.publish(Event(type="alert", data={}))
        assert received == []


class TestComposedFilters:
    def test_source_and_data_contains_both_match(self):
        bus = EventBus()
        received = []

        @EventFilter.where(source="agent-1", data_contains={"type": "result"})
        def handler(evt: Event):
            received.append(evt)

        bus.subscribe("output", handler)
        bus.publish(Event(type="output", source="agent-1", data={"type": "result"}))
        assert len(received) == 1

    def test_source_matches_but_data_does_not(self):
        bus = EventBus()
        received = []

        @EventFilter.where(source="agent-1", data_contains={"type": "result"})
        def handler(evt: Event):
            received.append(evt)

        bus.subscribe("output", handler)
        bus.publish(Event(type="output", source="agent-1", data={"type": "error"}))
        assert received == []

    def test_data_matches_but_source_does_not(self):
        bus = EventBus()
        received = []

        @EventFilter.where(source="agent-1", data_contains={"type": "result"})
        def handler(evt: Event):
            received.append(evt)

        bus.subscribe("output", handler)
        bus.publish(Event(type="output", source="agent-2", data={"type": "result"}))
        assert received == []
