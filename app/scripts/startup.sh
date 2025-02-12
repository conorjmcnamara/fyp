#!/bin/bash

docker compose build
docker compose --env-file ./backend/.env --env-file ./frontend/.env up