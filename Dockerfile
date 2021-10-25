FROM python:3.10.0-alpine3.14

RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev
RUN apk add curl git openssh
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
RUN ln -s $HOME/.poetry/bin/poetry /usr/bin/poetry
COPY pyproject.toml .
RUN pip3 install poetry
RUN poetry install