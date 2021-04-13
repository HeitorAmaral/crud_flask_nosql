FROM python:3.8
LABEL MAINTAINER="Heitor Amaral haamaral@topaz.com.br"
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . /app