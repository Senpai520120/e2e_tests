"""Unique names so tests never collide."""

import uuid


def unique(prefix: str) -> str:
    return f"e2e-{prefix}-{uuid.uuid4().hex[:8]}"