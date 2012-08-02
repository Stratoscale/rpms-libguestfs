#!/bin/bash -
# Additional custom requires for libguestfs package.
#
# Note this script is *ONLY* applicable to Fedora 17+ (ie. with UsrMove)
# since we now assume that /usr/lib{,64} and /lib{,64} are the same
# directory and hence that:
#
#   Requires: libfoo.so.1           <=>  /usr/lib/libfoo.so.1 exists
#   Requires: libfoo.so.1()(64bit)  <=>  /usr/lib64/libfoo.so.1 exists

original_find_requires="$1"
shift

# Get the list of files.
files=`sed "s/['\"]/\\\&/g"`

# Use ordinary find-requires first.
echo $files | tr [:blank:] '\n' | $original_find_requires

# Is supermin.d/hostfiles included in the list of files?
hostfiles=`echo $files | tr [:blank:] '\n' | grep 'supermin\.d/hostfiles$'`

if [ -z "$hostfiles" ]; then
    exit 0
fi

# Generate extra requires for libraries listed in hostfiles.
sofiles=`grep 'lib.*\.so\.' $hostfiles | fgrep -v '*'`
for f in $sofiles; do
    if [ -f "$f" ]; then
        if [[ "$f" =~ /lib64/(.*) ]]; then
            echo "${BASH_REMATCH[1]}()(64bit)"
        elif [[ "$f" =~ /lib/(.*) ]]; then
            echo "${BASH_REMATCH[1]}"
        fi
    fi
done
