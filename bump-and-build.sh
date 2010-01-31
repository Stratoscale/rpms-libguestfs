#!/bin/sh -

set -e

rpmdev-bumpspec -c "- Bump and rebuild." libguestfs.spec
cvs diff -u ||:
cvs ci -m "Bump and rebuild."
make tag && make build
