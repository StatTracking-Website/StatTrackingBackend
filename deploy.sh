#!/usr/bin/env bash
set -e

SERVER=${1:-"root@jesco.dev"}

echo "Building image..."
docker build -t stat-tracking-backend:v0 .

echo "Saving and compressing..."
docker save stat-tracking-backend:v0 | bzip2 > stat-tracking-backend.tar.bz2

echo "Transferring to $SERVER..."
scp stat-tracking-backend.tar.bz2 "$SERVER":~/stat-tracking-backend.tar.bz2

echo "Running deploy script on server..."
ssh "$SERVER" "bash ~/deploy_stat_tracking_backend.sh"

echo "Cleaning up local archive..."
rm stat-tracking-backend.tar.bz2

echo "Done."
