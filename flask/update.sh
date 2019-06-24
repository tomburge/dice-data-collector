#!/bin/bash
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