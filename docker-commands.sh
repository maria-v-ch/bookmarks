#!/bin/bash

case $1 in
  start)
    docker-compose up -d
    ;;
  build)
    docker-compose up -d --build
    ;;
  rebuild)
    docker-compose build
    docker-compose up -d
    ;;
  backup)
    docker-compose --profile backup run --rm backup
    ;;
  test)
    docker-compose --profile test run --rm test
    ;;
  *)
    echo "Usage: $0 {start|build|rebuild|backup|test}"
    exit 1
esac
