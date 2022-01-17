FROM python:3.8

WORKDIR /opt/app

COPY mediation .
COPY pyproject.toml .
COPY poetry.lock .

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH=${PATH}:/root/.poetry/bin

RUN poetry install

EXPOSE 9000
CMD ["poetry", "run", "python", "main.py"]
