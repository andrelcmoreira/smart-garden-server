FROM python:3.8

ARG SECRET_KEY
ARG ENV_TYPE

ENV SECRET_KEY=${SECRET_KEY}
# dev or prod
ENV ENV_TYPE=${ENV_TYPE}

EXPOSE 5000

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /app

ENTRYPOINT ["/bin/sh", "scripts/docker-entrypoint"]
