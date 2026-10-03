"""Small helpers shared by fixtures and tests."""

import uuid

from playwright.sync_api import Page

from config import User
from pages.login_page import LoginPage


def unique_name(prefix: str) -> str:
    """A name no other test run will use, for example "e2e_folder_3f9a1c2b".

    The app keeps everything the tests create, so every new user, folder or
    file gets a unique name. Then tests never collide with each other or with
    leftovers of an earlier run.
    """
    return f"e2e_{prefix}_{uuid.uuid4().hex[:8]}"


def sign_in(page: Page, user: User) -> Page:
    """Open /login/, sign in and wait until the app lets us in."""
    LoginPage(page).open().sign_in(user.username, user.password)
    # After a successful sign-in the app leaves /login/.
    page.wait_for_url(lambda url: "/login/" not in url)
    return page
