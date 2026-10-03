## What

## Why
Closes #

## Test cases
- TC-

## How to check
pytest -k "test_XX"

## Checklist
- [ ] Tests pass locally against `docker compose up`
- [ ] `black --check .` and `ruff check .` are clean
- [ ] No `time.sleep()` or fixed waits
- [ ] Tests clean up what they create (unique names, `yield` fixtures)
- [ ] `tools/test_cases.json` and `docs/test-cases.md` are updated
