"""Base class for all Page Objects."""

from typing import Self

from playwright.sync_api import Page


class BasePage:
    path = "/"

    def __init__(self, page: Page):
        self.page = page

    def open(self) -> Self:
        self.page.goto(self.path)
        return self