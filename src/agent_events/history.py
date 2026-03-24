"""
EventHistory — ring buffer of past events for replay and analytics.
"""

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

from .event import Event

if TYPE_CHECKING:
    from .bus import EventBus


class EventHistory:
    """Fixed-size ring buffer that records and replays events.

    Args:
        max_size: Maximum number of events to retain.  When the buffer is
                  full, the oldest event is automatically discarded.
    """

    def __init__(self, max_size: int = 500) -> None:
        self._max_size = max_size
        self._buffer: deque[Event] = deque(maxlen=max_size)
        self._total_recorded: int = 0

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record(self, event: Event) -> None:
        """Add *event* to the ring buffer."""
        self._buffer.append(event)
        self._total_recorded += 1

    # ------------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------------

    def query(
        self,
        event_type: str | None = None,
        source: str | None = None,
        limit: int = 10,
    ) -> list[Event]:
        """Return up to *limit* events matching the given filters.

        Filters are applied with AND semantics (both conditions must be met).
        Results are returned in **chronological order** (oldest first).

        Args:
            event_type: If given, only events with this type are returned.
            source:     If given, only events with this source are returned.
            limit:      Maximum number of events to return.
        """
        results: list[Event] = []
        for event in self._buffer:
            if event_type is not None and event.type != event_type:
                continue
            if source is not None and event.source != source:
                continue
            results.append(event)
            if len(results) >= limit:
                break
        return results

    # ------------------------------------------------------------------
    # Replay
    # ------------------------------------------------------------------

    def replay(
        self,
        bus: "EventBus",
        event_type: str | None = None,
    ) -> int:
        """Re-publish stored events to *bus*.

        Args:
            bus:        The :class:`~agent_events.EventBus` to publish into.
            event_type: If given, only events of this type are replayed.

        Returns:
            The number of events replayed.
        """
        count = 0
        for event in list(self._buffer):
            if event_type is not None and event.type != event_type:
                continue
            bus.publish(event)
            count += 1
        return count

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        """Return aggregate statistics about recorded events.

        Returns a dict with keys:
        - ``total_recorded``: int — cumulative count including evicted events
        - ``current_size``:   int — events currently in the buffer
        - ``by_type``:        dict[str, int] — event counts per type
        - ``oldest_timestamp``: float | None
        - ``newest_timestamp``: float | None
        """
        by_type: dict[str, int] = {}
        oldest: float | None = None
        newest: float | None = None

        for event in self._buffer:
            by_type[event.type] = by_type.get(event.type, 0) + 1
            if oldest is None or event.timestamp < oldest:
                oldest = event.timestamp
            if newest is None or event.timestamp > newest:
                newest = event.timestamp

        return {
            "total_recorded": self._total_recorded,
            "current_size": len(self._buffer),
            "by_type": by_type,
            "oldest_timestamp": oldest,
            "newest_timestamp": newest,
        }
