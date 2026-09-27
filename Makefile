.PHONY: tests lint clean help

DIRECTORY=.
EXCLUDED=.git,rxf.py
FLAKE8_IGNORED_RULES=E501,F405,F403,W504

lint:
	python3 -m flake8 --exclude=$(EXCLUDED) --ignore=$(FLAKE8_IGNORED_RULES) $(DIRECTORY)

tests: clean
	python3 -m pytest -n16 tests/core/ tests/test_exploit_scenarios.py tests/test_module_info.py
	python3 -m pytest -n16 tests/exploits/ tests/creds/ tests/encoders/ tests/generic/ tests/payloads/

clean:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete

help:
	@echo "    lint"
	@echo "        Check style with flake8."
	@echo "    test"
	@echo "        Run test suite"
	@echo "    clean"
	@echo "        Remove python artifacts."
