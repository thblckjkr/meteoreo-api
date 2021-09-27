#! /usr/bin/env sh

# Let the DB start
sleep 10;
# Run migrations
# masonite-orm migrate

# Install python dependencies
pip3 install -r requirements.txt

# TODO! Install sqlite or mysql depending on the config and the environment
