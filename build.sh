#!/bin/bash -e
source bash_env.sh
DIRECTORY=$(cd `dirname $0` && pwd)

# TODO: Containerize the build environment
pip install mkdocs-material
pip install mkdocs-awesome-pages-plugin
pip install plantuml-markdown
pip install mkdocs-minify-plugin
pip install plantuml-markdown

mkdocs build
mkdocs serve
