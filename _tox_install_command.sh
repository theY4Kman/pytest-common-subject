#!/bin/bash

# Setuptools may not be installed in users' environments. Uninstall it to ensure
# tests verify compatibility with environments that do not have setuptools.
pip uninstall -y setuptools

poetry install -v --no-root \
 && poetry run pip install "$@"
