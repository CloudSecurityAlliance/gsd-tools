#!/bin/bash

bundle config set path vendor/bundle
bundle install --jobs=1
bundle exec jekyll serve -w --host localhost --port 3000
