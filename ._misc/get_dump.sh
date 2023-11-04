#!/bin/bash

docker cp food-back:/app/media/. /home/<user>/foodgram/media
docker exec -t food-db pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
