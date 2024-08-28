from python:3.11-slim

WORKDIR /Nova-bot

COPY . ./
RUN pip install .
