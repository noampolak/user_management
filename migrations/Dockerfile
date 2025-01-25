FROM python:3.11 as poetryexporter
ENV PATH="${PATH}:/root/.local/bin"
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.4 python3 -

# Install Poetry
RUN pip install --no-cache-dir poetry

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN python -m venv --copies /app/venv
RUN . /app/venv/bin/activate && poetry install --no-root

FROM python:3.11 as final_image
COPY alembic.ini alembic.ini
COPY ./app /app
COPY ./migrations/ /migrations

COPY --from=poetryexporter /app/venv /app/venv/
ENV PATH /app/venv/bin:$PATH

ENV PYTHONPATH "${PYTHONPATH}:/"

CMD ["alembic", "upgrade", "head"]