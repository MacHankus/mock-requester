FROM python:3.11.6-alpine AS builder

RUN apt update -y

RUN apt install -y curl gnupg apt-transport-https
RUN apt-key adv --fetch-keys https://packages.microsoft.com/keys/microsoft.asc
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt update --fix-missing
RUN apt install build-essential libssl-dev -y
RUN apt install python3-dev -y
RUN ACCEPT_EULA=Y apt install msodbcsql17 -y
RUN ACCEPT_EULA=Y apt install mssql-tools -y
RUN apt install unixodbc-dev -y

RUN pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock ./
COPY src ./
COPY README.md ./

RUN apk add curl

RUN poetry config virtualenvs.create false \
    && poetry install

ENTRYPOINT ["python","./src/main.py"]
