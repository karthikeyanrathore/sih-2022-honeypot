#!/bin/bash

echo "build docker image ...."
docker build -t sih:latest . 

echo "running docker image ...."
docker run -it -d -p 5000:5000 sih

echo "http://localhost:5000/"


