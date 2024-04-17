#!/bin/bash

set -x
cd .

docker-compose up -d --scale app=5