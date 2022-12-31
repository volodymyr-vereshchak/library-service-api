FROM python:3.10-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY . /app
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
