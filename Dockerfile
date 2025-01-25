# Dockerfile
FROM python:3.11 as poetryexporter
ENV PATH="${PATH}:/root/.local/bin"

# Create a working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

# Install Poetry
RUN pip install --no-cache-dir poetry

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock


# CREATE VENV AND INSTALL DEPEENDENCIES
RUN python -m venv --copies /app/venv
RUN . /app/venv/bin/activate && poetry install --no-root

FROM python:3.11 as final_image

COPY ./app /app/
COPY --from=poetryexporter /app/venv /app/venv/
# Expose the port
EXPOSE 8000
ENV PATH /app/venv/bin:$PATH

ENV PYTHONPATH "${PYTHONPATH}:/"
WORKDIR /app

# Run the application
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]