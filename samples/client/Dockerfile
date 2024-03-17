FROM python:3.11.6-bullseye


WORKDIR /app

COPY samples/client/src src
COPY samples/client/requirements.txt requirements.txt

RUN ls -l 

RUN pip install -r requirements.txt

CMD ["python", "src/main.py"]