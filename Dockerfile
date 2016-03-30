FROM python:3.5
MAINTAINER roey.ghost@gmail.com

ADD . /opt/pushbullet-cli
RUN pip install /opt/pushbullet-cli
RUN rm -rf /opt/pushbullet-cli

ENTRYPOINT ["pb"]
