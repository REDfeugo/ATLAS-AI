# POSIX Skill Stubs

These modules outline how to port the Windows-first skills to macOS or Linux.
Each function currently raises `NotImplementedError` so contributors are forced to
consider platform nuances like accessibility permissions, sandboxing, and
available command-line tooling.

See `docs/14_CROSS_PLATFORM_ADAPTERS.md` for an in-depth guide.
