FROM python:3.11.6-slim-bullseye AS builder

RUN apt update -y && apt upgrade -y

RUN apt install curl -y
RUN apt install build-essential libssl-dev -y
RUN apt install python3-dev -y

RUN pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install

COPY README.md ./

COPY src src

ENTRYPOINT ["python","src/main.py"]
