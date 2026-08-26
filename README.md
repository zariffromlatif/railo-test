# railo-test

A sample Flask application used to validate [Railo](https://github.com/IWEBai/railo) — a deterministic, zero-hallucination vulnerability remediation engine.

## Vulnerabilities

This app intentionally contains security vulnerabilities for testing:

| CWE | Vulnerability | Location |
|:---|:---|:---|
| CWE-22 | Path Traversal | `app.py:download()` |
| CWE-89 | SQL Injection | `app.py:get_user()` |
| CWE-78 | Command Injection | `app.py:ping()` |
| CWE-798 | Hardcoded Secrets | `app.py:STRIPE_API_KEY` |

## Running Tests

```bash
pip install -r requirements.txt
pytest test_app.py -v
```