FROM python:3.11
LABEL authors="sushka"

WORKDIR /usr/src/app

RUN pip install poetry

COPY . /usr/src/app

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

ENTRYPOINT ["poetry", "run", "app"]