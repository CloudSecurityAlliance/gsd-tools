#!/usr/bin/env bash

removed_files=$(git diff --name-only --diff-filter=D 'HEAD^' | grep '\.json$' || true)

if [[ -n "$removed_files" ]]; then 
    echo "::group::removed files"
        echo "$removed_files"
    echo "::endgroup::"
    echo "You shall not change history."
    exit 1
fi
