#!/bin/bash -
# Additional custom requires for libguestfs package.

original_find_requires="$1"
shift

# Get the list of files.
files=`sed "s/['\"]/\\\&/g"`

# Use ordinary find-requires first.
echo $files | tr [:blank:] '\n' | $original_find_requires

# Is supermin.d/packages included in the list of files?
packages=`echo $files | tr [:blank:] '\n' | grep 'supermin\.d/packages$'`

if [ -z "$packages" ]; then
    exit 0
fi

# Generate one 'Requires:' line for each package listed in packages.
cat $packages
