FROM python:3.7.5-slim

RUN apt-get update && apt-get install -y git gcc python3-dev

ENV PYTHONUNBUFFERED=1 APP_HOME=/microservice/ CONFIGMAP_FILE="$APP_HOME"config-docker.yml

RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ADD requirement*.txt $APP_HOME
RUN pip install --upgrade pip && pip install -r requirements-docker.txt --pre

ADD . $APP_HOME

EXPOSE 8081

CMD ["gunicorn", "--worker-class", "gevent", "--workers", "1", "--log-level", "INFO", "--bind", "0.0.0.0:8081", "manage:app"]