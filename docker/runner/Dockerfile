FROM --platform=linux/amd64 python:3.10.2

WORKDIR runner/

ENV PYTHONPATH=.
ENV RUNNER_ALLOW_RUNASROOT="1"


# Install runner github
RUN apt update -y
# Download the latest runner package
RUN curl -o actions-runner-linux-x64-2.287.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.287.1/actions-runner-linux-x64-2.287.1.tar.gz
# Extract the installer
RUN tar xzf ./actions-runner-linux-x64-2.287.1.tar.gz

# Running container and then
## get your token here https://github.com/lunes-platform/lunespy/settings/actions/runners/new
## > ./config.sh --url https://github.com/lunes-platform/lunespy --token YOUR_TOKEN
## > ["./run.sh"]