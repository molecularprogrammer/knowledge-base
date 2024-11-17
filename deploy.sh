#!/bin/bash -e
source bash_env.sh
DIRECTORY=$(cd `dirname $0` && pwd)

mkdocs gh-deploy --force
