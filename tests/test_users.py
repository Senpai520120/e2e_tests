"""Admin panel: searching, creating and switching off users."""

from playwright.sync_api import Page, expect

import config
from helpers import unique_name
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.user_create_page import UserCreatePage
from pages.users_page import UsersPage


def test_12_admin_finds_user_by_search(admin_page: Page):
    """TC-12: searching by username shows that user and hides the others."""
    users_page = UsersPage(admin_page).open()

    users_page.search("demo_user05")

    expect(users_page.row("demo_user05")).to_be_visible()
    expect(users_page.row("demo_user06")).to_have_count(0)


def test_13_admin_creates_user(admin_page: Page):
    """TC-13: an admin creates a user and finds them in the list."""
    username = unique_name("user")
    create_page = UserCreatePage(admin_page).open()

    create_page.create_user(username, config.NEW_USER_PASSWORD)

    users_page = UsersPage(admin_page)
    expect(users_page.status_message).to_contain_text(f"User {username} created.")
    users_page.search(username)
    expect(users_page.row(username)).to_be_visible()


def test_14_new_user_can_sign_in(page: Page, new_user):
    """TC-14: a user created by an admin can sign in with their password."""
    login_page = LoginPage(page).open()

    login_page.sign_in(new_user.username, new_user.password)

    expect(HomePage(page).heading).to_have_text(
        f"You are signed in as {new_user.username}"
    )


def test_15_numeric_password_is_rejected(admin_page: Page):
    """TC-15: a password made only of digits is rejected, no user is created."""
    username = unique_name("weak")
    create_page = UserCreatePage(admin_page).open()

    create_page.create_user(username, "52012000")

    expect(admin_page.get_by_text("This password is entirely numeric.")).to_be_visible()
    users_page = UsersPage(admin_page).open()
    users_page.search(username)
    expect(users_page.nothing_found).to_be_visible()


def test_16_deactivated_user_cannot_sign_in(admin_page: Page, new_user, new_context):
    """TC-16: an admin switches a user off and that user can no longer sign in."""
    users_page = UsersPage(admin_page).open()
    users_page.search(new_user.username)

    users_page.deactivate_button(new_user.username).click()

    expect(users_page.status_message).to_contain_text(
        f"User {new_user.username} disabled."
    )
    expect(users_page.activate_button(new_user.username)).to_be_visible()

    # Try to sign in as that user in a separate browser.
    other_browser = new_context().new_page()
    login_page = LoginPage(other_browser).open()
    login_page.sign_in(new_user.username, new_user.password)
    expect(login_page.error_message).to_be_visible()
