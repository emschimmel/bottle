#!/usr/bin/env bash

docker build -t recommender-ui .
docker run -t -p 8084:8084 recommender-ui