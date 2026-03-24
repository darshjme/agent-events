"""Tests for the Event dataclass."""

import time
import uuid

import pytest

from agent_events import Event


class TestEventCreation:
    def test_required_fields(self):
        evt = Event(type="task.complete", data={"result": 42})
        assert evt.type == "task.complete"
        assert evt.data == {"result": 42}

    def test_auto_timestamp(self):
        before = time.time()
        evt = Event(type="x")
        after = time.time()
        assert before <= evt.timestamp <= after

    def test_auto_id_is_uuid4(self):
        evt = Event(type="x")
        parsed = uuid.UUID(evt.id, version=4)
        assert str(parsed) == evt.id

    def test_unique_ids(self):
        e1 = Event(type="x")
        e2 = Event(type="x")
        assert e1.id != e2.id

    def test_default_source_is_empty_string(self):
        evt = Event(type="x")
        assert evt.source == ""

    def test_explicit_source(self):
        evt = Event(type="x", source="agent-1")
        assert evt.source == "agent-1"

    def test_explicit_timestamp_preserved(self):
        ts = 1_000_000.0
        evt = Event(type="x", timestamp=ts)
        assert evt.timestamp == ts

    def test_explicit_id_preserved(self):
        custom_id = str(uuid.uuid4())
        evt = Event(type="x", id=custom_id)
        assert evt.id == custom_id


class TestEventSerialization:
    def test_to_dict_keys(self):
        evt = Event(type="ping", data={"k": "v"}, source="s")
        d = evt.to_dict()
        assert set(d.keys()) == {"type", "data", "source", "timestamp", "id"}

    def test_to_dict_values(self):
        evt = Event(type="ping", data={"k": "v"}, source="s")
        d = evt.to_dict()
        assert d["type"] == "ping"
        assert d["data"] == {"k": "v"}
        assert d["source"] == "s"
        assert d["timestamp"] == evt.timestamp
        assert d["id"] == evt.id

    def test_from_dict_roundtrip(self):
        original = Event(type="task.done", data={"x": 1}, source="agent-A")
        restored = Event.from_dict(original.to_dict())
        assert restored.type == original.type
        assert restored.data == original.data
        assert restored.source == original.source
        assert restored.timestamp == original.timestamp
        assert restored.id == original.id

    def test_from_dict_minimal(self):
        evt = Event.from_dict({"type": "minimal"})
        assert evt.type == "minimal"
        assert evt.data == {}
        assert evt.source == ""
