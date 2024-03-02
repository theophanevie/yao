FROM python:3.11-bookworm

RUN pip install poetry

ENV PYTHONUNBUFFERED=1

COPY src/ src
COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install --no-dev

CMD ["poetry", "run", "python", "yao/main.py"]
