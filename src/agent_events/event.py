"""
Event — base event dataclass for agent-events.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Event:
    """Base event class for the agent-events pub/sub system.

    Fields:
        type:      Event type string (e.g. "task.complete")
        data:      Arbitrary payload dict
        source:    Originating agent/component identifier
        timestamp: Unix timestamp (auto-set on creation)
        id:        Unique UUID4 string (auto-set on creation)
    """

    type: str
    data: dict[str, Any] = field(default_factory=dict)
    source: str = ""
    timestamp: float = field(default=0.0)
    id: str = field(default="")

    def __post_init__(self) -> None:
        if not self.timestamp:
            self.timestamp = time.time()
        if not self.id:
            self.id = str(uuid.uuid4())

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Return a plain-dict representation of this event."""
        return {
            "type": self.type,
            "data": self.data,
            "source": self.source,
            "timestamp": self.timestamp,
            "id": self.id,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Event":
        """Reconstruct an Event from a dict (e.g. after JSON round-trip)."""
        evt = cls(
            type=d["type"],
            data=d.get("data", {}),
            source=d.get("source", ""),
            timestamp=d.get("timestamp", 0.0),
            id=d.get("id", ""),
        )
        # Preserve the original timestamp/id if they were provided
        if "timestamp" in d and d["timestamp"]:
            evt.timestamp = d["timestamp"]
        if "id" in d and d["id"]:
            evt.id = d["id"]
        return evt
