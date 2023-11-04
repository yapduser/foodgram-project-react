#!/bin/bash

docker cp /home/<user>/foodgram/media/. food-back:/app/media
cat dump_04-11-2023_02_06_31.sql | docker exec -i food-db psql -U postgres
