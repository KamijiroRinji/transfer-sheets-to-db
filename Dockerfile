FROM python:3.7-slim

ENV POETRY_VERSION=1.1.5
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN apt-get update && pip install -U pip && pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true \
  && poetry install --no-interaction --no-ansi --no-dev

COPY . /app

CMD ["python", "-u", "main.py"]
