FROM python:3.8

WORKDIR /opt/app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

COPY mediation .
COPY pyproject.toml .
COPY poetry.lock .

ENV SECRET_ID = ptl/app-credentials/gp-connect-record-access-testing-app/non-prod/CLIENT_ID_INT
ENV PATH=${PATH}:/root/.poetry/bin

RUN poetry install

EXPOSE 9000

CMD ["poetry", "run", "python", "main.py"]
