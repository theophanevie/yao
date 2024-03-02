FROM python:3.11-bookworm

RUN apt update && apt-get install -y ffmpeg

RUN pip install poetry

ENV PYTHONUNBUFFERED=1

COPY yao/ yao
COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install --no-dev

CMD ["poetry", "run", "python", "yao/main.py"]
