#!/bin/bash

BASE_DIR=$(pwd)
BASE_URL_TEST="http://localhost:8000"
export $(cat .env | xargs) && docker-compose up -d && cd $BASE_DIR && export BASE_URL=$BASE_URL_TEST && python tests/flash_sale.py