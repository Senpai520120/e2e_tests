import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.p1
@pytest.mark.auth
def test_anonymous_is_redirected_to_login(page: Page):
    """AUTH-09"""
    page.goto("/")

    expect(page).to_have_url(re.compile(r"/login/\?next=/$"))