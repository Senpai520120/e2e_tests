"""Who can open the admin panel and the file manager."""

import re

from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.users_page import UsersPage


def test_08_regular_user_gets_403_on_admin_panel(user_page: Page):
    """TC-08: a user without the admin role gets "access denied" on /manage/."""
    user_page.goto("/manage/")

    expect(user_page.get_by_role("heading", name="403 — access denied")).to_be_visible()


def test_09_admin_opens_admin_panel(admin_page: Page):
    """TC-09: an admin opens the user list at /manage/."""
    users_page = UsersPage(admin_page).open()

    expect(users_page.heading).to_be_visible()
    expect(users_page.row("demo_admin")).to_be_visible()


def test_10_regular_user_does_not_see_admin_links(user_page: Page):
    """TC-10: a regular user has no "Users", "Roles" and "Audit" links in the header."""
    home_page = HomePage(user_page).open()

    expect(home_page.header_link("Files")).to_be_visible()
    expect(home_page.header_link("Users")).to_have_count(0)
    expect(home_page.header_link("Roles")).to_have_count(0)
    expect(home_page.header_link("Audit")).to_have_count(0)


def test_11_anonymous_user_cannot_open_file_manager(page: Page):
    """TC-11: an anonymous user who opens /files/ is sent to sign in."""
    page.goto("/files/")

    expect(page).to_have_url(re.compile(r"/login/\?next=/files/$"))
