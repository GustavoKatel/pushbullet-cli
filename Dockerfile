FROM python:3-alpine
MAINTAINER gbritosampaio@gmail.com

ADD setup.py /opt/pushbullet-cli/setup.py
ADD pushbullet_cli /opt/pushbullet-cli/pushbullet_cli
RUN pip install /opt/pushbullet-cli && rm -rf /opt/pushbullet-cli

ENTRYPOINT ["pb"]
