#!/bin/sh
set -e

# Том монтируется от root — вернём владельца
if [ -d /app/logs ]; then
    chown -R botuser:botuser /app
fi

exec gosu botuser "$@"