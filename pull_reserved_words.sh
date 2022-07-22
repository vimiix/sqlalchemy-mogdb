#!/usr/bin/env sh

## This was developed on macOS and may not directly translate to
## other platforms.

curl "https://docs.mogdb.io/zh/mogdb/v3.0/2-keywords/" \
    | grep -E '<td align="left">' \
    | sed 's/.*>\(.*\)<.*/\1/' \
    | grep -vE 'reserved|col-name|type-func-name' \
    | sed 's/^\([A-Z0-9_]*\).*/"\1",/' \
    | paste -s -d' ' - \
    | fold -s -w 70 \
    | awk '{print "    "$0}' \
    | tr 'A-Z' 'a-z'
