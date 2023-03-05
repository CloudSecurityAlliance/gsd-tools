#!/bin/bash

bundle config set path vendor/bundle
bundle install --jobs=1
bundle exec jekyll clean
bundle exec jekyll serve --livereload --safe --host localhost --port 3000
