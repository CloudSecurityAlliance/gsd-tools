#!/bin/bash

SECURITYLIST=~/src/securitylist
CVELIST=~/src/cvelist
DWFLIST=~/src/dwflist

pushd .
# Check out or update the repos
cd $SECURITYLIST && git pull
cd $CVELIST && git pull
cd $DWFLIST && git pull
# Update NVD
popd
./update_nvd.py $SECURITYLIST
# Update cvelist
./update_repo.py $SECURITYLIST $CVELIST MITRE
# Update dwflist
./update_repo.py $SECURITYLIST $DWFLIST DWF
