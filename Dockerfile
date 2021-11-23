FROM python:3.8
LABEL maintainer=="Tsheri Sherpa"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -yq update
RUN apt-get -yq install python3-dev default-libmysqlclient-dev build-essential

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD . /flaskapp

WORKDIR /flaskapp

RUN cp /flaskapp/.env.example /flaskapp/.env

RUN chmod +x /flaskapp/run.py
# CMD ["nohup", "python", "run.py", "&"]
EXPOSE 8000