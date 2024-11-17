#!/bin/bash -e

# Export all variables
set -a
ROOT_DIRECTORY=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Docker dependency
sudo apt-get install docker.io
VERSION="docker --version"
echo Installed ${VERSION}
