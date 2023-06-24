FROM python:3.11.3

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /src/
WORKDIR /src/
RUN git config --global --add safe.directory /src/
RUN pre-commit install-hooks