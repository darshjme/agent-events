"""
EventBus — central pub/sub coordinator for agent-events.
"""

from __future__ import annotations

import queue
from collections import defaultdict
from typing import Callable

from .event import Event


class _Subscription:
    """Internal wrapper that pairs a handler with its priority."""

    __slots__ = ("handler", "priority")

    def __init__(self, handler: Callable[[Event], None], priority: int) -> None:
        self.handler = handler
        self.priority = priority


class EventBus:
    """Central pub/sub coordinator.

    Supports both synchronous (publish) and asynchronous (publish_async /
    process_queue) dispatch, with per-subscription priorities.

    Higher ``priority`` values are invoked **first**.
    """

    def __init__(self, max_queue_size: int = 1000) -> None:
        # event_type -> list of _Subscription (sorted by priority desc)
        self._subscribers: dict[str, list[_Subscription]] = defaultdict(list)
        self._queue: queue.Queue[Event] = queue.Queue(maxsize=max_queue_size)

    # ------------------------------------------------------------------
    # Subscription management
    # ------------------------------------------------------------------

    def subscribe(
        self,
        event_type: str,
        handler: Callable[[Event], None],
        priority: int = 0,
    ) -> None:
        """Register *handler* to receive events of *event_type*.

        Handlers with higher *priority* are called before lower-priority ones.
        """
        subs = self._subscribers[event_type]
        # Avoid duplicate registrations for the same handler
        if any(s.handler is handler for s in subs):
            return
        subs.append(_Subscription(handler, priority))
        # Keep sorted: highest priority first
        subs.sort(key=lambda s: s.priority, reverse=True)

    def unsubscribe(
        self,
        event_type: str,
        handler: Callable[[Event], None],
    ) -> None:
        """Remove *handler* from *event_type* subscriptions (no-op if absent)."""
        subs = self._subscribers.get(event_type)
        if subs is None:
            return
        self._subscribers[event_type] = [s for s in subs if s.handler is not handler]

    def subscriber_count(self, event_type: str) -> int:
        """Return the number of handlers currently subscribed to *event_type*."""
        return len(self._subscribers.get(event_type, []))

    def clear(self, event_type: str | None = None) -> None:
        """Remove all handlers.

        If *event_type* is given, only that type's handlers are cleared;
        otherwise **all** subscriptions are removed.
        """
        if event_type is None:
            self._subscribers.clear()
        else:
            self._subscribers.pop(event_type, None)

    # ------------------------------------------------------------------
    # Synchronous dispatch
    # ------------------------------------------------------------------

    def publish(self, event: Event) -> int:
        """Dispatch *event* synchronously to all matching handlers.

        Returns the number of handlers that were called.
        """
        subs = self._subscribers.get(event.type, [])
        for sub in list(subs):  # snapshot in case a handler mutates the list
            sub.handler(event)
        return len(subs)

    # ------------------------------------------------------------------
    # Asynchronous dispatch (queue-based)
    # ------------------------------------------------------------------

    def publish_async(self, event: Event) -> None:
        """Enqueue *event* for later processing; returns immediately.

        Raises ``queue.Full`` if the queue is at capacity.
        """
        self._queue.put_nowait(event)

    def process_queue(self, max_events: int = 100) -> int:
        """Drain up to *max_events* from the async queue, dispatching each.

        Returns the total number of handler invocations across all processed
        events.
        """
        total_calls = 0
        for _ in range(max_events):
            try:
                event = self._queue.get_nowait()
            except queue.Empty:
                break
            total_calls += self.publish(event)
        return total_calls
