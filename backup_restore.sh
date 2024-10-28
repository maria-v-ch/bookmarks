#!/bin/bash

backup() {
    echo "Creating backup..."
    docker-compose run --rm backup
    echo "Backup created successfully."
}

restore() {
    if [ -z "$1" ]; then
        echo "Please provide a backup file name."
        exit 1
    fi

    echo "Restoring from backup: $1"
    docker-compose exec -T db psql -U postgres -d bookmarks < "./backups/$1"
    echo "Restore completed."
}

case "$1" in
    backup)
        backup
        ;;
    restore)
        restore "$2"
        ;;
    *)
        echo "Usage: $0 {backup|restore <filename>}"
        exit 1
esac
