#!/bin/bash

echo -en "building docker image..."
docker build -t forpytest  ./img-ubuntu-sshd/ &> /dev/null
echo -e "\t\tdone"

echo -en "running docker container for test..."
docker run -p 22022:22 --name pytestcontainer --rm -d forpytest &> /dev/null
echo -e "\tdone"

pushd src
py.test -s -v test.py
popd

echo -en "stopping docker container..."
docker stop pytestcontainer &> /dev/null
echo -e "\t\tdone"

echo -en "removing docker image..."
docker rmi forpytest &> /dev/null
echo -e "\t\tdone"
