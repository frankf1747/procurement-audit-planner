# Part B: the standalone agent harness on localhost
PY := .venv/bin/python

.PHONY: setup run test

setup:            ## create .venv and install everything (Part A + harness)
	test -d .venv || python3 -m venv .venv
	$(PY) -m pip install -q -r requirements.txt
	test -f .env || cp .env.example .env

run:              ## start the web app at http://localhost:8000
	$(PY) -m uvicorn harness.app:app --host 127.0.0.1 --port 8000

test:             ## harness tests (scripted model, no API calls) and the skill tests
	$(PY) -m pytest -q tests
	$(PY) .claude/skills/extract-rules/tests/test_verify_quotes.py
	$(PY) .claude/skills/risk-assessment/tests/test_build_register.py
