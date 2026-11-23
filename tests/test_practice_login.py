import re

from playwright.sync_api import Page, expect


def submit_login(page: Page, url: str, username: str, password: str) -> None:
    page.goto(url)
    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Submit").click()


def test_login_with_valid_credentials(
    page: Page,
    practice_login_url: str,
    practice_username: str,
    practice_password: str,
) -> None:
    submit_login(page, practice_login_url, practice_username, practice_password)

    expect(page).to_have_url(re.compile(r".*/logged-in-successfully/?$"))
    expect(page.get_by_role("heading", name="Logged In Successfully")).to_be_visible()
    expect(page.get_by_role("link", name="Log out")).to_be_visible()


def test_login_rejects_invalid_username(
    page: Page,
    practice_login_url: str,
    practice_password: str,
) -> None:
    submit_login(page, practice_login_url, "invalid-user", practice_password)

    expect(page.locator("#error")).to_have_text("Your username is invalid!")


def test_login_rejects_invalid_password(
    page: Page,
    practice_login_url: str,
    practice_username: str,
) -> None:
    submit_login(page, practice_login_url, practice_username, "invalid-password")

    expect(page.locator("#error")).to_have_text("Your password is invalid!")
