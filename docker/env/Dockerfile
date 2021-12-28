
FROM python:3.10.0-alpine3.14

ENV PYTHONPATH=.
RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev curl git openssh
COPY requirements.txt .
RUN pip3 install -r requirements.txt