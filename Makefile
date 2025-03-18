install: uv.lock
	uv sync

test:
	uv run pytest tests/
