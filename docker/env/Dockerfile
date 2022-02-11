FROM python:3.10.0-alpine3.14

ENV PYTHONPATH=.
COPY requirements.txt .

RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev curl git openssh
RUN pip3 install --upgrade pip -r requirements.txt
RUN git config --global core.editor 'code --wait'