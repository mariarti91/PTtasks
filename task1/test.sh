#!/bin/bash

echo -en "building docker image..."
docker build -t forpytest  ./img-ubuntu-sshd/ &> /dev/null
echo -e "\t\tdone"

echo -en "running docker container for test..."
docker run -p 22022:22 --name pytestcontainer -d forpytest &> /dev/null
echo -e "\tdone"

py.test -s -v test.py

echo -en "stopping docker container..."
docker stop pytestcontainer &> /dev/null
echo -e "\t\tdone"

echo -en "removing docker container..."
docker rm pytestcontainer &> /dev/null
echo -e "\t\tdone"

echo -en "removing docker image..."
docker rmi forpytest &> /dev/null
echo -e "\t\tdone"
