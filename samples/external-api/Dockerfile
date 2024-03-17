FROM python:3.11.6-bullseye


WORKDIR /app

COPY samples/external-api/src src
COPY samples/external-api/requirements.txt requirements.txt

RUN ls -l 

RUN apt install curl

RUN pip install -r requirements.txt

CMD ["python", "src/main.py"]