FROM python:3.9-slim

RUN apt-get update && apt-get install -y 

RUN apt-get install libgl1 -y

RUN apt-get install libgl1-mesa-glx -y

RUN apt-get install libglib2.0-0 -y

ENV PYTHONBUFFERED True

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app