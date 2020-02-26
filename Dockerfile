FROM python:3-alpine

LABEL maintainer="Tsheri Sherpa" 

COPY . /flaskapp

WORKDIR /flaskapp

RUN apk add build-base wget openblas-dev

RUN apk add python3-dev openssl-dev libffi-dev musl-dev gcc && pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

CMD ["python", "run.py"]
