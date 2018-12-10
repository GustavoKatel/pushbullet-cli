#!/bin/sh

set -x # debug
set -e # exit if any command fail

echo "$DOCKER_PASSWORD" | docker login -u "gustavokatel" --password-stdin

if [ "$TRAVIS_BRANCH" == "master" ]; then
    RELEASE="master"
else
    RELEASE="latest"
fi

docker tag pushbullet-cli gustavokatel/pushbullet-cli:$RELEASE

docker push gustavokatel/pushbullet-cli:$RELEASE
