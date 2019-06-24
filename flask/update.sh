#!/bin/bash
# this script updates the appliance from github
cd
cd dice-data-collector
docker-compose down
cd ..
rm -rf dice-data-collector
docker system prune -a
cd
git clone https://github.com/tomburge/dice-data-collector.git
cd dice-data-collector
docker-compose up -d --build