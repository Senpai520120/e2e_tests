"""Settings that depend on the environment."""

import os

PASSWORD = os.getenv("E2E_PASSWORD", "demo-password-123")