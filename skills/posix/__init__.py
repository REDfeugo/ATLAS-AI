"""POSIX stubs mirroring the Windows skill interface."""

from __future__ import annotations


def not_implemented(*_: object, **__: object) -> dict:
    """Raise a friendly error to signal missing implementation."""

    raise NotImplementedError(
        "POSIX skills are not yet implemented. See docs/14_CROSS_PLATFORM_ADAPTERS.md."
    )
