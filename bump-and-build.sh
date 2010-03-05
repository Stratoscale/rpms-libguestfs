#!/bin/sh -

set -e

rpmdev-bumpspec -r -c "- Bump and rebuild." libguestfs.spec
cvs diff -u ||:
echo Press RETURN to commit or ^C to exit.
read
cvs ci -m "Bump and rebuild."
make tag && make build && make update
