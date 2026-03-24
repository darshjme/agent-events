# Changelog

All notable changes to **agent-events** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-03-24

### Added
- `Event` dataclass with auto UUID4 `id` and Unix `timestamp`, `to_dict` / `from_dict` helpers.
- `EventBus` with synchronous `publish`, async `publish_async` / `process_queue`, priority-ordered subscriptions, `subscriber_count`, and `clear`.
- `EventFilter` composable decorator factory (`source`, `data_contains`, `min_priority` predicates).
- `EventHistory` ring buffer with `record`, `query`, `replay`, and `stats`.
- Full pytest test suite (22+ tests, 100 % component coverage).
- Zero runtime dependencies — Python 3.10+ standard library only.

[Unreleased]: https://github.com/darshjme-codes/agent-events/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/darshjme-codes/agent-events/releases/tag/v0.1.0
