#!/usr/bin/env bash

git diff --name-only --diff-filter=ACMRT 'HEAD^' |
    grep '\.json$' |
    while read -r i; do
        if ! python -m json.tool "$i" > /dev/null; then
            echo "Wrong Syntax: $i"
            exit 1
        fi
    done
