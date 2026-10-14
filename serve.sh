#!/bin/bash
set -e

DIRECTORY="$(cd "$(dirname "$0")" && pwd)"

docker run --rm -it \
  -v "${DIRECTORY}:/workspace" \
  -p 8000:8000 \
  ghcr.io/molecularprogrammer/container-properdocs:latest \
  properdocs serve --dev-addr=0.0.0.0:8000