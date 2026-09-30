"""Demo users created by `manage.py seed_demo_users`."""

from dataclasses import dataclass

import config


@dataclass(frozen=True)
class DemoUser:
    username: str
    password: str = config.PASSWORD


ADMIN = DemoUser("demo_admin")
STAFF = DemoUser("demo_staff")
USER = DemoUser("demo_user")
INACTIVE = DemoUser("demo_inactive")