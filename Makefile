install:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt
	cd frontend && npm install

dev:
	. .venv/bin/activate && uvicorn backend.app:app --reload --port 8000

test:
	. .venv/bin/activate && pip install -U pip && pip install -r requirements.txt
	. .venv/bin/activate && pytest -q
