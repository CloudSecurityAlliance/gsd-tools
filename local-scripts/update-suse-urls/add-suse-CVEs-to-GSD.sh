#!/bin/bash

# Run from /gsd-database/ root directory

# consumes a list of CVEs

# CVE-YEAR-INTEGER
# YEAR/INTxxx/GSD-YEAR-INTEGER.json

input=$1

while IFS= read -r line
do
    GSDID=`echo $line | sed 's/CVE/GSD/'`
    YEAR=`echo $line | cut -d"-" -f2`
    INT=`echo $line | cut -d"-" -f3`
    DIR=`echo $INT | sed 's/[0-9][0-9][0-9]$/xxx/'`
    FILENAME="$GSDID.json"
    FILE="$YEAR/$DIR/$FILENAME"
    URL="https://www.suse.com/security/cve/$line.html"
    TEMP=$(mktemp)

    if [ -f "$FILE" ]; then
      # Check if the key already exists
      FOUND="true"
      # If no GSD.references[] array exiosts you'll get an error
      FOUND=`jq -e '.GSD.references|any(. == "'$URL'")' $FILE`
      if [ $FOUND == "true" ]; then
        echo -n "."
      else
        # So if false or null we add the url
        echo ""
        # Kurt checked, there are no SUSE URL's in this form in the CVE namespace
  	    # jq converts flopats to ints, e.g. 10.0 to 10
        jq --arg new "$URL" '.GSD.references? += [$new]' $FILE > $TEMP
        # print fix, assumes repo location
        ../gsd-tools/local-scripts/print-json.py $TEMP
        # fix float to int problem intentioanlly obtuse to be readable
        # ": 6.0,
        # ": 10.0,
        sed 's/": 1,$/": 1.0,/' $TEMP | sed 's/": 2,$/": 2.0,/' | sed 's/": 3,$/": 3.0,/' | sed 's/": 4,$/": 4.0,/' | sed 's/": 5,$/": 5.0,/' | sed 's/": 6,$/": 6.0,/' | sed 's/": 7,$/": 7.0,/' | sed 's/": 8,$/": 8.0,/' | sed 's/": 9,$/": 9.0,/' | sed 's/": 10,$/": 10.0,/' | sed 's/": 1$/": 1.0/' | sed 's/": 2$/": 2.0/' | sed 's/": 3$/": 3.0/' | sed 's/": 4$/": 4.0/' | sed 's/": 5$/": 5.0/' | sed 's/": 6$/": 6.0/' | sed 's/": 7$/": 7.0/' | sed 's/": 8$/": 8.0/' | sed 's/": 9$/": 9.0/' | sed 's/": 10$/": 10.0/' > $FILE
        rm -f $TEMP
        # done-o-dial
        echo "Updated $FILE"
      fi
    else
      echo "ERROR: $FILE does not exist."
    fi

done < "$input"
