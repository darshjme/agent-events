"""
EventFilter — composable filtering decorator for event handlers.
"""

from __future__ import annotations

import functools
from typing import Any, Callable

from .event import Event


class EventFilter:
    """Factory for filtering decorators applied to event handler functions.

    Usage::

        @EventFilter.where(source="agent-1")
        def on_agent1_event(event: Event) -> None:
            ...

        @EventFilter.where(data_contains={"status": "done"})
        def on_done(event: Event) -> None:
            ...

        @EventFilter.where(source="agent-1", data_contains={"type": "result"})
        def on_agent1_result(event: Event) -> None:
            ...

    Filters are evaluated **before** the handler is called.  If the event
    does not satisfy all conditions the handler is silently skipped.
    """

    @staticmethod
    def where(
        *,
        source: str | None = None,
        data_contains: dict[str, Any] | None = None,
        min_priority: int | None = None,
    ) -> Callable[[Callable[[Event], None]], Callable[[Event], None]]:
        """Return a decorator that gates the handler on the given predicates.

        Args:
            source:        Only handle events whose ``event.source`` matches.
            data_contains: Only handle events whose ``event.data`` contains
                           **all** key-value pairs in this dict (deep equality).
            min_priority:  Only handle events whose ``event.data`` contains a
                           numeric ``"priority"`` field >= *min_priority*.
        """

        def decorator(
            func: Callable[[Event], None],
        ) -> Callable[[Event], None]:
            @functools.wraps(func)
            def wrapper(event: Event) -> None:
                # --- source filter ---
                if source is not None and event.source != source:
                    return

                # --- data_contains filter ---
                if data_contains is not None:
                    for key, expected in data_contains.items():
                        if event.data.get(key) != expected:
                            return

                # --- min_priority filter ---
                if min_priority is not None:
                    event_priority = event.data.get("priority")
                    if not isinstance(event_priority, (int, float)):
                        return
                    if event_priority < min_priority:
                        return

                func(event)

            # Tag the wrapper so EventBus identity checks still work
            wrapper._original_handler = func  # type: ignore[attr-defined]
            return wrapper

        return decorator
