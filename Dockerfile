FROM python:3.6
LABEL maintainer "Timothy Ko <tk2@illinois.edu>"
RUN locale-gen ru_RU.UTF-8
RUN update-locale LANG=ru_RU.UTF-8 LC_MESSAGES=POSIX
RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV="docker"
EXPOSE 5000
