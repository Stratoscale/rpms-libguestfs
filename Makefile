
all: build

mkfile_path := $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))
mkfile_dir:=$(shell cd $(shell dirname $(mkfile_path)); pwd)
current_dir:=$(notdir $(mkfile_dir))

build:
	mkdir -p output
	sudo chown -R 9001:9001 output
	sudo docker run --rm -i --name=rpm-builder -v `pwd`:/home/makerpm/$(current_dir) rackattack-nas.dc1:5000/stratoscale/fedora-binary-rpm-builder-base:latest /bin/bash -c "make -f Makefile.libguestfs -C /home/makerpm/$(current_dir)"
	sudo chown -R ${USER}:${USER} output

submit:
	# This target is called by jenkins-slave
	#     # Only submit when there is no label cleancandidate or clean
	SOLVENT_CLEAN=True 2>/dev/null solvent printlabel --product rpms --thisProject | egrep 'clean(candidate)?$$' || SOLVENT_CLEAN=True solvent submitproduct rpms output

approve:
	# This target is called by jenkins-slave
	#     # Only approve when there is no label clean
	SOLVENT_CLEAN=True 2>/dev/null osmosis listlabels $(shell git rev-parse HEAD) --objectStores osmosis.dc1:1010 | egrep 'clean$$' || SOLVENT_CLEAN=True solvent approve --product rpms --ignoreFailureOnLocalObjectStore

clean:
	rm -rf output
