
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY README.md .
COPY poetry.lock .
COPY src/ ./src/
RUN python3 -m venv .venv
RUN .venv/bin/python3 -m pip install --upgrade pip
RUN .venv/bin/python3 -m pip install poetry
RUN .venv/bin/poetry install --only main



CMD .venv/bin/python -O -m src