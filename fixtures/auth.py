"""Pages already signed in as a given user."""

import pytest
from playwright.sync_api import Page

from data import users
from data.users import DemoUser
from pages.login_page import LoginPage


def _login(page: Page, user: DemoUser) -> Page:
    LoginPage(page).open().login(user.username, user.password)
    return page


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Opened login page, nobody signed in."""
    return LoginPage(page).open()


@pytest.fixture
def admin_page(page: Page) -> Page:
    return _login(page, users.ADMIN)


@pytest.fixture
def user_page(page: Page) -> Page:
    return _login(page, users.USER)