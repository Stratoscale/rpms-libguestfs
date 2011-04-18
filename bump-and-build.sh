#!/bin/sh -

set -e

rpmdev-bumpspec -r -c "- Bump and rebuild." libguestfs.spec
git diff ||:
echo "Press ENTER to commit, push and rebuild."
read line
fedpkg commit -m "Bump and rebuild." -p
fedpkg build
