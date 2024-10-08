ifdef OS
	PYTHON ?= .venv/Scripts/python.exe
	TYPE_CHECK_COMMAND ?= echo Pytype package doesn't support Windows OS
else
	PYTHON ?= .venv/bin/python
	TYPE_CHECK_COMMAND ?= ${PYTHON} -m pytype --config=pytype.cfg src
endif

SETTINGS_FILENAME = pyproject.toml

.PHONY: secure
secure:
	uv run bandit -r src --config ${SETTINGS_FILENAME}
