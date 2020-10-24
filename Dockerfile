FROM python:3.7.9-alpine
LABEL maintainer="gbritosampaio@gmail.com"

ADD . /opt/pushbullet-cli

RUN apk add -v build-base libffi-dev openssl-dev && \
pip install /opt/pushbullet-cli && \
rm -rf /opt/pushbullet-cli && \
apk del build-base libffi-dev openssl-dev

ENTRYPOINT ["pb"]
