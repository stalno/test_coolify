
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies including wget for healthchecks
# Устанавливаем curl, wget и другие зависимости
RUN apt-get update && \
    apt-get install -y curl wget \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY README.md .
COPY poetry.lock .
COPY src/ ./src/
RUN python3 -m venv .venv
RUN .venv/bin/python3 -m pip install --upgrade pip
RUN .venv/bin/python3 -m pip install poetry
RUN .venv/bin/poetry install --only main

ENV PORT 80
EXPOSE $PORT

CMD .venv/bin/python -O -m src