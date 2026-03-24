# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅ Yes    |

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Send an email to **darshjme@gmail.com** with:

- A description of the vulnerability
- Steps to reproduce it
- The potential impact
- Any suggested fix (optional but appreciated)

You will receive an acknowledgement within **48 hours** and a resolution
timeline within **7 days**.

## Scope

agent-events is a pure in-process library with zero network I/O and zero
runtime dependencies. The attack surface is limited to:

- Malicious event `data` payloads deserialized via `Event.from_dict`
- Handler callbacks that execute arbitrary user-supplied code (by design —
  callers are responsible for handler safety)

## Disclosure Policy

We follow [Responsible Disclosure](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html).
Coordinated disclosure with a CVE (if applicable) will be published after a
patch is released.
