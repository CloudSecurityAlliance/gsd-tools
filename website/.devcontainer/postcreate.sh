#!/bin/bash

bundle config set path vendor/bundle
bundle install --jobs=1
bundle exec jekyll serve -w --safe --host localhost --port 3000 --trace
