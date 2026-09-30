"""Role names as they exist in the application."""

from enum import StrEnum


class Role(StrEnum):
    ADMIN = "admin"
    USER = "user"