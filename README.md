# E2E tests for Django-application-e2e

Browser tests (Python + pytest + Playwright) for
[Django-application-e2e](https://github.com/Senpai520120/Django-application-e2e):
sign-in, the admin panel at `/manage/` and the file manager at `/files/`.

43 test cases, `TC-01` … `TC-43`, each with its own automated test.
The list is in [docs/test-cases.md](docs/test-cases.md) and in GitHub issues
with the `test-case` label.

Last run: all tests pass in **Chromium, Firefox and WebKit**, except TC-40,
which shows a known bug (see below).

## What the tests protect

The most serious things that can break, and the tests that catch them.

| What can go wrong | Tests |
| --- | --- |
| **Someone gets in without a valid password**: wrong password, unknown user, switched-off user | TC-02 … TC-05 |
| **The error message tells which usernames exist** | TC-04 |
| **A user stays signed in after sign-out or after being switched off** | TC-06, TC-38 |
| **A user without the admin role reaches admin pages**, by link or by sending the form straight to the server | TC-08, TC-10, TC-35, TC-36 |
| **An admin locks themselves out** by removing their own admin role or switching themselves off | TC-20, TC-37 |
| **A role change has no trace**: who changed what, for whom | TC-21, TC-39 |
| **Switching a user off has no trace** | TC-40, *known bug #142* |
| **Size limit is checked wrong**: exactly the limit must pass, one byte more must not | TC-41, TC-33 |
| **Data is lost or overwritten**: a file is replaced by another with the same name, a download differs from the upload, a duplicate folder appears | TC-24, TC-30, TC-34 |
| **A path leads outside the file storage** (`?path=../..`) | TC-42 |
| **A sign-in link sends the user to another site** (`?next=https://...`) | TC-43 |
| Everyday scenarios: search, create a user, roles, folders, upload, rename, delete | the rest |

How the access tests work: TC-35 and TC-36 do not click in the page. They send
the form straight to the server with the user's session and a valid CSRF token,
the way an attacker would. So they prove that the server refuses, not only that
the button is hidden.

### Known bug

**#142: switching a user off is not written to the audit log.** The app records
only role changes. TC-40 checks this and is marked `xfail` ("expected to fail"):
pytest shows it as `x` and the run stays green. When the app is fixed, pytest
reports the test as unexpectedly passing, and the marker must be removed.

### Not covered, and why

- Switching off a **superuser**: the demo data has no superuser account.
- Path traversal in all its forms (`..`, absolute paths, null bytes, bad names)
  is checked in detail by the app's own unit tests (`tests/test_files_paths.py`).
  Here one browser-level check (TC-42) is enough.
- Running the tests in CI on every pull request: a separate task, issue #4.

## Requirements

- Python 3.11+
- Docker Desktop, to run the app under test

## 1. Start the app

In the folder of the **app** repository:

```bash
cp .env.example .env    # then put any long random string into SECRET_KEY
docker compose up --build
```

The app opens at http://127.0.0.1:8000 with demo accounts already created:
`demo_admin`, `demo_user`, `demo_inactive`, all with the password `demo-password-123`.

> Run the tests only against a local copy of the app. They sign in with
> well-known demo passwords and create users, folders and files.

## 2. Install the tests

In the folder of **this** repository:

```bash
python -m venv .venv
.venv\Scripts\activate             # macOS / Linux: source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium firefox webkit
```

## 3. Run

```bash
pytest                                   # all tests in Chromium
pytest -v                                # with test names
pytest tests/test_login.py               # one file
pytest -k test_05                        # one test by its number
pytest --headed --slowmo 500             # watch the browser, slowed down
pytest --base-url http://127.0.0.1:8001  # another copy of the app
```

In all three browsers (Chrome, Firefox and Safari engines):

```bash
pytest --browser chromium --browser firefox --browser webkit
```

The result line looks like `126 passed, 3 xfailed`: 42 tests × 3 browsers pass,
and TC-40 is the known bug in each browser.

A failed test leaves a trace, a screenshot and a video in `test-results/`.
Open the trace with:

```bash
playwright show-trace test-results/<test folder>/trace.zip
```

## Settings

| Variable | Default | What for |
| --- | --- | --- |
| `E2E_PASSWORD` | `demo-password-123` | password of the demo accounts |
| `E2E_MAX_FILE_SIZE` | `5242880` (5 MB) | must equal `FILE_MANAGER_MAX_FILE_SIZE` of the app |

## Project layout

```
pages/          Page Objects: HOW to work with each page (locators and actions)
tests/          the tests: WHAT we check, one test per test case
conftest.py     fixtures: signed-in pages, a second admin browser, a new user,
                an empty working folder
config.py       settings and demo accounts
helpers.py      unique_name(), sign_in(), send_form()
tools/          test_cases.json and the script that turns it into issues
docs/           test-cases.md
```

Rules that keep the tests readable and stable:

- a test only does steps and checks; locators live in `pages/`;
- a Page Object never checks results; `expect` is used only in tests;
- every test works with data of its own (unique names), so the order does not matter;
- no `time.sleep()`: `expect(...)` waits by itself until the page is ready;
- a Page Object method that sends a form waits for the server's answer
  (`BasePage.submit()`), so the next step never leaves the page too early.

## Lint

```bash
black .
ruff check --fix .
```

## Test cases → GitHub issues

```bash
python tools/create_test_case_issues.py --dry-run    # preview
python tools/create_test_case_issues.py              # create missing issues
python tools/create_test_case_issues.py --markdown   # rebuild docs/test-cases.md
```
