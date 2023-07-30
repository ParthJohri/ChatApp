#!/bin/bash

# Install Poetry
curl -sSL https://install.python-poetry.org | python -

# Activate Poetry virtual environment
source $HOME/.poetry/env

# Install project dependencies using Poetry
poetry install
