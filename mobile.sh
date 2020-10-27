#!/bin/bash

docker rm mobile -f
docker rmi mobile -f
docker build -t mobile .
docker run -d --name mobile -p 5000:5000 mobile
