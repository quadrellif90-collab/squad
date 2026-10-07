#!/usr/bin/env bash
set -e
TARGET="$HOME/.agents/squad"
mkdir -p "$TARGET"
cp -r config disciplines src "$TARGET/"
echo "Squad installed to $TARGET"
echo "Edit $TARGET/config/config.yml and run: orca mcp add squad python $TARGET/src/squad_server.py"
