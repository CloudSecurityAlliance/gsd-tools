#!/bin/bash

GSDLIST=~/gsd/gsd-database
CVELIST=~/gsd/cvelist

pushd .
# Check out or update the repos
cd $GSDLIST && git pull
cd $CVELIST && git pull
# Update NVD
popd
./update_nvd.py $GSDLIST
./update_gitlab.py $GSDLIST
# Update cvelist
./update_repo.py $GSDLIST $CVELIST "cve.org"
