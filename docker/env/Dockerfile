FROM python:alpine
ENV PYTHONPATH=.

RUN apk add --no-cache curl zsh git gcc musl-dev
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN ln -sv /root/.poetry/bin/poetry /usr/bin/poetry
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
RUN git config --global core.editor 'code --wait'
