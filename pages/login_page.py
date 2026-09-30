"""Sign-in page at /login/."""

from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/login/"

    def __init__(self, page):
        super().__init__(page)
        self.username_input = ...
        self.password_input = ...
        self.submit_button = ...
        self.error_message = ...

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()