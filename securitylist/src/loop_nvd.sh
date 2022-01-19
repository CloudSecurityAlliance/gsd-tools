#!/bin/bash

# the first time we load the NVD data, we need to run it in a loop to get
# all the data, it's sparsed out in the beginning

GSDLIST=~/gsd/gsd-database

while true;
do
./update_nvd.py $GSDLIST
sleep 1
done
