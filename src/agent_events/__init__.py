"""
agent-events: Event bus and pub/sub system for multi-agent coordination.
Zero dependencies. Pure Python 3.10+.
"""

from .event import Event
from .bus import EventBus
from .filter import EventFilter
from .history import EventHistory

__version__ = "0.1.0"
__all__ = ["Event", "EventBus", "EventFilter", "EventHistory"]
