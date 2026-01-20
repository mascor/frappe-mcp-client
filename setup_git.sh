#!/bin/bash
set -e

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    git init
    echo "Initialized empty Git repository"
else
    echo "Git repository already initialized"
fi

# Set remote origin
REMOTE_URL="https://github.com/mascor/frappe-mcp-client"

if git remote | grep -q "^origin$"; then
    echo "Remote 'origin' already exists. Updating URL..."
    git remote set-url origin "$REMOTE_URL"
else
    echo "Adding remote 'origin'..."
    git remote add origin "$REMOTE_URL"
fi

echo "Remote 'origin' set to $REMOTE_URL"
