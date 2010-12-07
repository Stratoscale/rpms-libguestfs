# If you have trouble building locally ('make local') try adding
#   %libguestfs_buildnet 1
# to your ~/.rpmmacros file.

# Enable to build using a network repo
# Default is disabled
%if %{defined libguestfs_buildnet}
%global buildnet %{libguestfs_buildnet}
%else
%global buildnet 0
%endif 

# Enable to make the appliance use virtio_blk
# Default is enabled
%if %{defined libguestfs_virtio}
%global with_virtio %{libguestfs_virtio}
%else
%global with_virtio 1
%endif 

# Enable to run tests during check
# Default is enabled
%if %{defined libguestfs_runtests}
%global runtests %{libguestfs_runtests}
%else
%global runtests 1
%endif

Summary:       Access and modify virtual machine disk images
Name:          libguestfs
Epoch:         1
Version:       1.7.19
Release:       15%{?dist}
License:       LGPLv2+
Group:         Development/Libraries
URL:           http://libguestfs.org/
Source0:       http://libguestfs.org/download/1.7-development/%{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root

# Disable FUSE tests, not supported in Koji at the moment.
Patch0:        libguestfs-1.7.13-no-fuse-test.patch

# Disable test for RHBZ#576879 which wasn't working (or bug reappeared).
Patch1:        0001-regressions-Disable-test-for-576879.patch
# Add --with-febootstrap-yum-config option.
Patch2:        0002-Add-with-febootstrap-yum-config.patch
# Fix a bug in quoting.
Patch3:        0003-appliance-Don-t-quote-the-exclude-parameters.patch
BuildRequires: autoconf, automake, libtool, gettext-devel

# Basic build requirements:
BuildRequires: /usr/bin/pod2man
BuildRequires: /usr/bin/pod2text
BuildRequires: febootstrap >= 3.1-5
BuildRequires: hivex-devel >= 1.2.2
BuildRequires: augeas-devel >= 0.5.0
BuildRequires: readline-devel
BuildRequires: genisoimage
BuildRequires: libxml2-devel
BuildRequires: qemu-kvm >= 0.10-7
BuildRequires: createrepo
BuildRequires: glibc-static
BuildRequires: libselinux-devel
BuildRequires: fuse-devel
BuildRequires: pcre-devel
BuildRequires: file-devel
BuildRequires: libvirt-devel
BuildRequires: po4a
BuildRequires: gperf
BuildRequires: db4-utils
BuildRequires: cpio

# This is only needed for RHEL 5 because readline-devel doesn't
# properly depend on it, but doesn't do any harm on other platforms:
BuildRequires: ncurses-devel

# Build requirements for the appliance (see 'make.sh.in' in the source):
BuildRequires: kernel, bash, coreutils, lvm2, ntfs-3g, util-linux-ng
BuildRequires: MAKEDEV, net-tools, augeas-libs, file
BuildRequires: module-init-tools, procps, strace, iputils
BuildRequires: dosfstools, zerofree, lsof, scrub, libselinux
BuildRequires: parted, e2fsprogs, btrfs-progs, gfs2-utils
BuildRequires: hfsplus-tools, nilfs-utils, reiserfs-utils
BuildRequires: jfsutils, xfsprogs
BuildRequires: vim-minimal
BuildRequires: binutils
BuildRequires: cryptsetup-luks
%ifarch %{ix86} x86_64
BuildRequires: grub, ntfsprogs
%endif

# Must match the above set of BuildRequires exactly!
Requires:      kernel, bash, coreutils, lvm2, ntfs-3g, util-linux-ng
Requires:      MAKEDEV, net-tools, augeas-libs, file
Requires:      module-init-tools, procps, strace, iputils
Requires:      dosfstools, zerofree, lsof, scrub, libselinux
Requires:      parted, e2fsprogs, btrfs-progs, gfs2-utils
Requires:      hfsplus-tools, nilfs-utils, reiserfs-utils
Requires:      jfsutils, xfsprogs
Requires:      vim-minimal
Requires:      binutils
Requires:      cryptsetup-luks
%ifarch %{ix86} x86_64
Requires:      grub, ntfsprogs
%endif

# These are only required if you want to build the bindings for
# different languages:
BuildRequires: ocaml
BuildRequires: ocaml-findlib-devel
BuildRequires: perl-devel
BuildRequires: perl-Test-Simple
BuildRequires: perl-Test-Pod
BuildRequires: perl-Test-Pod-Coverage
BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: perl-String-ShellQuote
BuildRequires: perl-XML-Writer
BuildRequires: perl-libintl
BuildRequires: python-devel
BuildRequires: ruby-devel
BuildRequires: rubygem-rake
BuildRequires: java >= 1.5.0
BuildRequires: jpackage-utils
BuildRequires: java-devel
BuildRequires: php-devel

# For libguestfs-tools:
BuildRequires: perl-Sys-Virt
BuildRequires: qemu-img

# Runtime requires:
Requires:      qemu-kvm >= 0.12
Requires:      febootstrap >= 3.1-5

# For libguestfs-test-tool.
Requires:      genisoimage

# For core inspection API.
Requires:      db4-utils

# Provide our own custom requires for the supermin appliance.
Source1:       libguestfs-find-requires.sh
%global _use_internal_dependency_generator 0
%global __find_provides %{_rpmconfigdir}/find-provides
%global __find_requires %{SOURCE1} %{_rpmconfigdir}/find-requires


%description
Libguestfs is a library for accessing and modifying guest disk images.
Amongst the things this is good for: making batch configuration
changes to guests, getting disk used/free statistics (see also:
virt-df), migrating between virtualization systems (see also:
virt-p2v), performing partial backups, performing partial guest
clones, cloning guests and changing registry/UUID/hostname info, and
much else besides.

Libguestfs uses Linux kernel and qemu code, and can access any type of
guest filesystem that Linux and qemu can, including but not limited
to: ext2/3/4, btrfs, FAT and NTFS, LVM, many different disk partition
schemes, qcow, qcow2, vmdk.

Libguestfs provides ways to enumerate guest storage (eg. partitions,
LVs, what filesystem is in each LV, etc.).  It can also run commands
in the context of the guest.

Libguestfs is a library that can be linked with C and C++ management
programs.

See also the 'guestfish' package for shell scripting and command line
access, and '%{name}-mount' for mounting guest filesystems on the
host using FUSE.

For Perl bindings, see 'perl-Sys-Guestfs'.

For OCaml bindings, see 'ocaml-libguestfs-devel'.

For Python bindings, see 'python-libguestfs'.

For Ruby bindings, see 'ruby-libguestfs'.

For Java bindings, see 'libguestfs-java-devel'.

For PHP bindings, see 'php-libguestfs'.


%package devel
Summary:       Development tools and libraries for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      pkgconfig


%description devel
%{name}-devel contains development tools and libraries
for %{name}.


%package -n guestfish
Summary:       Shell for accessing and modifying virtual machine disk images
Group:         Development/Tools
License:       GPLv2+
Requires:      %{name} = %{epoch}:%{version}-%{release}
#Requires:      /usr/bin/emacs #theoretically, but too large
Requires:      /usr/bin/hexedit
Requires:      /usr/bin/less
Requires:      /usr/bin/man
Requires:      /bin/vi


%description -n guestfish
Guestfish is the Filesystem Interactive SHell, for accessing and
modifying virtual machine disk images from the command line and shell
scripts.


%package mount
Summary:       Mount guest filesystems on the host using FUSE and libguestfs
Group:         Development/Tools
License:       GPLv2+
Requires:      %{name} = %{epoch}:%{version}-%{release}


%description mount
The guestmount command lets you mount guest filesystems on the
host using FUSE and %{name}.


%package tools-c
Summary:       System administration tools for virtual machines
Group:         Development/Tools
License:       GPLv2+
Requires:      %{name} = %{epoch}:%{version}-%{release}

# Obsolete and replace earlier packages.
Provides:      virt-cat = %{epoch}:%{version}-%{release}
Obsoletes:     virt-cat < %{epoch}:%{version}-%{release}
Provides:      virt-df = %{epoch}:%{version}-%{release}
Obsoletes:     virt-df < %{epoch}:%{version}-%{release}
Provides:      virt-inspector = %{epoch}:%{version}-%{release}
Obsoletes:     virt-inspector < %{epoch}:%{version}-%{release}

# RHBZ#514309
Provides:      virt-df2 = %{epoch}:%{version}-%{release}
Obsoletes:     virt-df2 < %{epoch}:%{version}-%{release}


%description tools-c
This package contains miscellaneous system administrator command line
tools for virtual machines.

Note that you should install %{name}-tools (which pulls in
this package).  This package is only used directly when you want
to avoid dependencies on Perl.


%package tools
Summary:       System administration tools for virtual machines
Group:         Development/Tools
License:       GPLv2+
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      %{name}-tools-c = %{epoch}:%{version}-%{release}
# NB: Only list deps here which are not picked up automatically.
Requires:      perl(Sys::Virt)
Requires:      perl(String::ShellQuote)
Requires:      perl(XML::Writer)
Requires:      perl(Win::Hivex)
Requires:      qemu-img


%description tools
This package contains miscellaneous system administrator command line
tools for virtual machines.

Virt-cat is a command line tool to display the contents of a file in a
virtual machine.

Virt-df is a command line tool to display free space on virtual
machine filesystems.  Unlike other tools, it doesn’t just display the
amount of space allocated to a virtual machine, but can look inside
the virtual machine to see how much space is really being used.  It is
like the df(1) command, but for virtual machines, except that it also
works for Windows virtual machines.

Virt-edit is a command line tool to edit the contents of a file in a
virtual machine.

Virt-filesystems is a command line tool to display the filesystems,
partitions, block devices, LVs, VGs and PVs found in a disk image
or virtual machine.  It replaces the deprecated programs
virt-list-filesystems and virt-list-partitions with a much more
capable tool.

Virt-inspector examines a virtual machine and tries to determine the
version of the OS, the kernel version, what drivers are installed,
whether the virtual machine is fully virtualized (FV) or
para-virtualized (PV), what applications are installed and more.

Virt-ls is a command line tool to list out files in a virtual machine.

Virt-make-fs is a command line tool to build a filesystem out of
a collection of files or a tarball.

Virt-rescue provides a rescue shell for making interactive,
unstructured fixes to virtual machines.

Virt-resize can resize existing virtual machine disk images.

Virt-tar is an archive, backup and upload tool for virtual machines.

Virt-win-reg lets you look inside the Windows Registry for
Windows virtual machines.


%package -n ocaml-%{name}
Summary:       OCaml bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}


%description -n ocaml-%{name}
ocaml-%{name} contains OCaml bindings for %{name}.

This is for toplevel and scripting access only.  To compile OCaml
programs which use %{name} you will also need ocaml-%{name}-devel.


%package -n ocaml-%{name}-devel
Summary:       OCaml bindings for %{name}
Group:         Development/Libraries
Requires:      ocaml-%{name} = %{epoch}:%{version}-%{release}


%description -n ocaml-%{name}-devel
ocaml-%{name}-devel contains development libraries
required to use the OCaml bindings for %{name}.


%package -n perl-Sys-Guestfs
Summary:       Perl bindings for %{name} (Sys::Guestfs)
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# RHBZ#523547
Requires:      perl(XML::XPath)
# RHBZ#652587 - for backwards compat with the old name
Provides:      perl-%{name} = %{epoch}:%{version}-%{release}
Obsoletes:     perl-%{name} < %{epoch}:%{version}-%{release}


%description -n perl-Sys-Guestfs
perl-Sys-Guestfs contains Perl bindings for %{name} (Sys::Guestfs).


%package -n python-%{name}
Summary:       Python bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description -n python-%{name}
python-%{name} contains Python bindings for %{name}.


%package -n ruby-%{name}
Summary:       Ruby bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      ruby(abi) = 1.8
Requires:      ruby
Provides:      ruby(guestfs) = %{version}

%{!?ruby_sitelib: %define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}
%{!?ruby_sitearch: %define ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

%description -n ruby-%{name}
ruby-%{name} contains Ruby bindings for %{name}.


%package java
Summary:       Java bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      java >= 1.5.0
Requires:      jpackage-utils

%description java
%{name}-java contains Java bindings for %{name}.

If you want to develop software in Java which uses %{name}, then
you will also need %{name}-java-devel.


%package java-devel
Summary:       Java development package for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      %{name}-java = %{epoch}:%{version}-%{release}

%description java-devel
%{name}-java-devel contains the tools for developing Java software
using %{name}.

See also %{name}-javadoc.


%package javadoc
Summary:       Java documentation for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      %{name}-java = %{epoch}:%{version}-%{release}
Requires:      jpackage-utils

%description javadoc
%{name}-javadoc contains the Java documentation for %{name}.


%package -n php-%{name}
Summary:       PHP bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      php

%description -n php-%{name}
php-%{name} contains PHP bindings for %{name}.


%prep
%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
aclocal -I m4
autoreconf -i -f
rm -f appliance/make.sh

mkdir -p daemon/m4


%build
%if %{buildnet}
%define extra %{nil}
%else
mkdir repo
find /var/cache/yum -type f -name '*.rpm' -print0 | xargs -0 cp -t repo
createrepo repo
cat > yum.conf <<EOF
[main]
cachedir=/var/cache/yum
debuglevel=1
logfile=/var/log/yum.log
retries=20
obsoletes=1
gpgcheck=0
assumeyes=1
reposdir=/dev/null

[local]
name=local
baseurl=file://$(pwd)/repo
failovermethod=priority
enabled=1
gpgcheck=0
EOF
%define extra --with-febootstrap-yum-config=$(pwd)/yum.conf
echo "==== /etc/yum.conf ===="
cat /etc/yum.conf
echo "==== our yum.conf ===="
cat yum.conf
%endif

./configure \
  --prefix=%{_prefix} --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --sysconfdir=%{_sysconfdir} \
  --with-qemu="qemu-kvm qemu-system-%{_build_arch} qemu" \
%if %{with_virtio}
  --with-drive-if=virtio \
%endif
  %{extra}

# This ensures that /usr/sbin/chroot is on the path.  Not needed
# except for RHEL 5, it shouldn't do any harm on other platforms.
export PATH=/usr/sbin:$PATH

# 'INSTALLDIRS' ensures that perl libs are installed in the vendor dir
# not the site dir.
make INSTALLDIRS=vendor %{?_smp_mflags}

# Useful for debugging appliance problems.
for f in appliance/supermin.d/*.img; do
    b=`basename $f`
    echo "==== $b ===="
    ls -l $f
    cpio -itv < $f
done
echo "==== hostfiles ===="
ls -l appliance/supermin.d/hostfiles
cat appliance/supermin.d/hostfiles
echo "======================================================================"


%check
# Enable debugging - very useful if a test does fail, although
# it produces masses of output in the build.log.
export LIBGUESTFS_DEBUG=1

# Uncomment one of these, depending on whether you want to
# do a very long and thorough test ('make check') or just
# a quick test to see if things generally work.

# Tracking test issues:
# BZ       archs        branch reason
# 494075   ppc, ppc64          openbios bug causes "invalid/unsupported opcode"
# 504273   ppc, ppc64          "no opcode defined"
# 505109   ppc, ppc64          "Boot failure! No secondary bootloader specified"
# 502058   i386, x86-64 F-11   need to boot with noapic (WORKAROUND ENABLED)
# 502074   i386         all    commands segfault randomly
# 503236   i386         F-12   cryptomgr_test at doublefault_fn
# 507066   all          F-12   sequence of chroot calls (FIXED)
# 513249   all          F-12   guestfwd broken in qemu (FIXED)
# 516022   all          F-12   virtio-net gives "Network is unreachable" errors
#                                 (FIXED)
# 516096   ?            F-11   race condition in swapoff/blockdev --rereadpt
# 516543   ?            F-12   qemu-kvm segfaults when run inside a VM (FIXED)
# 548121   all          F-13   udevsettle command is broken (WORKAROUND)
# 553689   all          F-13   missing SeaBIOS (FIXED)
# 563103   all          F-13   glibc incorrect emulation of preadv/pwritev
#                                 (sort of FIXED)
# 567567   32-bit       all    guestfish xstrtol test failure on 32-bit (FIXED)
# 575734   all          F-14   microsecond resolution for blkid cache (FIXED)
# 630583   all          all    kernel hangs setting scheduler to noop
# 630777   all          F-15   task lvm blocked for more than 120 seconds
#                                 (FIXED)

# This test fails because we build the ISO after encoding the checksum
# of the ISO in the test itself.  Need to fix the test to work out the
# checksum at runtime.
export SKIP_TEST_CHECKSUM_DEVICE=1

# Work around 'test-getlogin_r.c:55: assertion failed' in Gnulib tests.
pushd daemon/tests
borked=test-getlogin_r
make $borked
rm $borked
touch $borked
chmod +x $borked
popd

%if %{runtests}
make check
%endif


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Delete static libraries, libtool files.
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs.a
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs.la

find $RPM_BUILD_ROOT -name perllocal.pod -delete
find $RPM_BUILD_ROOT -name .packlist -delete
find $RPM_BUILD_ROOT -name '*.bs' -delete
find $RPM_BUILD_ROOT -name 'bindtests.pl' -delete

rm $RPM_BUILD_ROOT%{python_sitearch}/libguestfsmod.a
rm $RPM_BUILD_ROOT%{python_sitearch}/libguestfsmod.la

if [ "$RPM_BUILD_ROOT%{python_sitearch}" != "$RPM_BUILD_ROOT%{python_sitelib}" ]; then
   mkdir -p $RPM_BUILD_ROOT%{python_sitelib}
   mv $RPM_BUILD_ROOT%{python_sitearch}/guestfs.py* \
     $RPM_BUILD_ROOT%{python_sitelib}/
fi

# Remove static-linked Java bindings.
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs_jni.a
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs_jni.la

# Move installed documentation back to the source directory so
# we can install it using a %%doc rule.
mv $RPM_BUILD_ROOT%{_docdir}/libguestfs installed-docs

# Remove Japanese manpages, since these are not translated fully at
# the moment.  When these are translated properly we intend to add
# them back.
rm -rf $RPM_BUILD_ROOT%{_mandir}/ja/man{1,3}/

# Find locale files.
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/libguestfs-test-tool
%{_libdir}/guestfs/
%{_libdir}/libguestfs.so.*
%{_libexecdir}/libguestfs-test-tool-helper
%{_mandir}/man1/libguestfs-test-tool.1*


%files devel
%defattr(-,root,root,-)
%doc AUTHORS BUGS ChangeLog HACKING TODO README RELEASE-NOTES
%doc examples/*.c
%doc installed-docs/*
%{_libdir}/libguestfs.so
%{_mandir}/man3/guestfs.3*
%{_mandir}/man3/guestfs-examples.3*
%{_mandir}/man3/libguestfs.3*
%{_includedir}/guestfs.h
%{_libdir}/pkgconfig/libguestfs.pc


%files -n guestfish
%defattr(-,root,root,-)
%doc recipes/
%{_bindir}/guestfish
%{_mandir}/man1/guestfish.1*
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/guestfish-bash-completion.sh


%files mount
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/guestmount
%{_mandir}/man1/guestmount.1*


%files tools-c
%defattr(-,root,root,-)
%{_bindir}/virt-cat
%{_mandir}/man1/virt-cat.1*
%{_bindir}/virt-df
%{_mandir}/man1/virt-df.1*
%{_bindir}/virt-filesystems
%{_mandir}/man1/virt-filesystems.1*
%{_bindir}/virt-inspector
%{_mandir}/man1/virt-inspector.1*
%{_bindir}/virt-ls
%{_mandir}/man1/virt-ls.1*
%{_bindir}/virt-rescue
%{_mandir}/man1/virt-rescue.1*


%files tools
%defattr(-,root,root,-)
%{_bindir}/virt-edit
%{_mandir}/man1/virt-edit.1*
%{_bindir}/virt-list-filesystems
%{_mandir}/man1/virt-list-filesystems.1*
%{_bindir}/virt-list-partitions
%{_mandir}/man1/virt-list-partitions.1*
%{_bindir}/virt-make-fs
%{_mandir}/man1/virt-make-fs.1*
%{_bindir}/virt-resize
%{_mandir}/man1/virt-resize.1*
%{_bindir}/virt-tar
%{_mandir}/man1/virt-tar.1*
%{_bindir}/virt-win-reg
%{_mandir}/man1/virt-win-reg.1*


%files -n ocaml-%{name}
%defattr(-,root,root,-)
%doc README
%{_libdir}/ocaml/guestfs
%exclude %{_libdir}/ocaml/guestfs/*.a
%exclude %{_libdir}/ocaml/guestfs/*.cmxa
%exclude %{_libdir}/ocaml/guestfs/*.cmx
%exclude %{_libdir}/ocaml/guestfs/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files -n ocaml-%{name}-devel
%defattr(-,root,root,-)
%doc ocaml/examples/*.ml
%{_libdir}/ocaml/guestfs/*.a
%{_libdir}/ocaml/guestfs/*.cmxa
%{_libdir}/ocaml/guestfs/*.cmx
%{_libdir}/ocaml/guestfs/*.mli
%{_mandir}/man3/guestfs-ocaml.3*


%files -n perl-Sys-Guestfs
%defattr(-,root,root,-)
%doc perl/examples
%{perl_vendorarch}/*
%{_mandir}/man3/Sys::Guestfs.3pm*
%{_mandir}/man3/Sys::Guestfs::Lib.3pm*


%files -n python-%{name}
%defattr(-,root,root,-)
%doc README
%doc python/examples/*.py
%{python_sitearch}/*
%{python_sitelib}/*.py
%{python_sitelib}/*.pyc
%{python_sitelib}/*.pyo
%{_mandir}/man3/guestfs-python.3*


%files -n ruby-%{name}
%defattr(-,root,root,-)
%doc README
%doc ruby/examples/*.rb
%{ruby_sitelib}/guestfs.rb
%{ruby_sitearch}/_guestfs.so
%{_mandir}/man3/guestfs-ruby.3*


%files java
%defattr(-,root,root,-)
%doc README
%{_libdir}/libguestfs_jni*.so.*
%{_datadir}/java/*.jar


%files java-devel
%defattr(-,root,root,-)
%doc README
%{_libdir}/libguestfs_jni*.so


%files javadoc
%defattr(-,root,root,-)
%doc README
%{_datadir}/javadoc/%{name}-java-%{version}


%files -n php-%{name}
%defattr(-,root,root,-)
%doc php/README-PHP
%dir %{_sysconfdir}/php.d
%{_sysconfdir}/php.d/guestfs_php.ini
%{_libdir}/php/modules/guestfs_php.so


%changelog
* Tue Dec  7 2010 Richard Jones <rjones@redhat.com> - 1:1.7.19-15
- Rebuild appliance with febootstrap 3.1-5 because we accidentally
  reopened RHBZ#654638.

* Mon Dec  6 2010 Richard Jones <rjones@redhat.com> - 1:1.7.19-14
- Rebuild appliance properly using febootstrap 3.1 and alternate yum repo.

* Sun Dec  5 2010 Richard Jones <rjones@redhat.com> - 1:1.7.19-1
- New upstream development version 1.7.19.
- Appliance building in this version has been substantially rewritten
  and this requires febootstrap >= 3.0 to build.
- createrepo no longer required.
- Supermin appliance is the default.

* Wed Dec  1 2010 Richard Jones <rjones@redhat.com> - 1:1.7.18-1
- New upstream development version 1.7.18.

* Tue Nov 30 2010 Richard Jones <rjones@redhat.com> - 1:1.7.17-1
- New upstream development version 1.7.17.

* Fri Nov 26 2010 Richard Jones <rjones@redhat.com> - 1:1.7.16-1
- New upstream development version 1.7.16.
- guestfish no longer requires pod2text, hence no longer requires perl.
- Require febootstrap >= 2.11.

* Fri Nov 26 2010 Richard Jones <rjones@redhat.com> - 1:1.7.15-2
- New upstream development version 1.7.15.
- Split out new libguestfs-tools-c package from libguestfs-tools.
  . This is so that the -tools-c package can be pulled in by people
    wanting to avoid a dependency on Perl, while -tools pulls in everything
    as before.
  . The C tools currently are: cat, df, filesystems, fish, inspector, ls,
    mount, rescue.
  . guestfish still requires pod2text which requires perl.  This will be
    rectified in the next release.
  . libguestfs-tools no longer pulls in guestfish.
- guestfish also depends on: less, man, vi
- Add BR db4-utils (although since RPM needs it, it not really necessary).
- Runtime requires on db4-utils should be on core lib, not tools package.
- Change all "Requires: perl-Foo" to "Requires: perl(Foo)".

* Thu Nov 25 2010 Richard Jones <rjones@redhat.com> - 1:1.7.14-1
- New upstream development version 1.7.14.

* Wed Nov 24 2010 Richard Jones <rjones@redhat.com> - 1:1.7.13-3
- New upstream development version 1.7.13.
- New manual pages containing example code.
- Ship examples for C, OCaml, Ruby, Python.
- Don't ship HTML versions of man pages.
- Rebase no-fuse-test patch to latest version.

* Tue Nov 23 2010 Richard Jones <rjones@redhat.com> - 1:1.7.12-1
- New upstream development version 1.7.12.
- New tool: virt-filesystems.  virt-list-filesystems and virt-list-partitions
  are deprecated, but still included in the package.

* Wed Nov 17 2010 Richard Jones <rjones@redhat.com> - 1:1.7.11-1
- New upstream development version 1.7.11.
- Fix Source0 URL which had pointed to the 1.5 directory.
- virt-inspector is not a dependency of guestmount.

* Wed Nov 17 2010 Richard Jones <rjones@redhat.com> - 1:1.7.10-1
- New upstream development version 1.7.10.

* Tue Nov 16 2010 Richard Jones <rjones@redhat.com> - 1:1.7.9-1
- New upstream development version 1.7.9.

* Mon Nov 15 2010 Richard Jones <rjones@redhat.com> - 1:1.7.8-1
- New upstream development version 1.7.8.
- Add Obsoletes so perl-Sys-Guestfs overrides perl-libguestfs (RHBZ#652587).

* Mon Nov 15 2010 Richard Jones <rjones@redhat.com> - 1:1.7.7-1
- New upstream development version 1.7.7.
- Rename perl-libguestfs as perl-Sys-Guestfs (RHBZ#652587).

* Sat Nov 13 2010 Richard Jones <rjones@redhat.com> - 1:1.7.6-1
- New upstream development version 1.7.6.

* Sat Nov 13 2010 Richard Jones <rjones@redhat.com> - 1:1.7.5-2
- New upstream development version 1.7.5.
- Remove hand-installation of Ruby bindings.
- Remove upstream patch.

* Thu Nov 11 2010 Richard Jones <rjones@redhat.com> - 1:1.7.4-2
- New upstream development version 1.7.4.
- ocaml-xml-light is no longer required.
- Remove guestfs-actions.h and guestfs-structs.h.  Libguestfs now
  only exports a single <guestfs.h> header file.
- Add patch to fix broken Perl test.
- Remove workaround for RHBZ#563103.

* Mon Nov  8 2010 Richard Jones <rjones@redhat.com> - 1:1.7.3-1
- New upstream development version 1.7.3.
- Add AUTHORS file from tarball.

* Fri Nov  5 2010 Richard Jones <rjones@redhat.com> - 1:1.7.2-1
- New upstream development version 1.7.2.
- Add requires ruby to ruby-libguestfs package.

* Wed Nov  3 2010 Richard Jones <rjones@redhat.com> - 1:1.7.1-1
- New upstream development version 1.7.1.
- Add BR gperf.

* Tue Nov  2 2010 Richard Jones <rjones@redhat.com> - 1:1.7.0-1
- New upstream development branch and version 1.7.0.

* Fri Oct 29 2010 Richard Jones <rjones@redhat.com> - 1:1.5.26-1
- New upstream development version 1.5.26.

* Thu Oct 28 2010 Richard Jones <rjones@redhat.com> - 1:1.5.25-1
- New upstream development version 1.5.25.
- Rewritten virt-inspector.
- Requires febootstrap >= 2.10.
- New virt-inspector requires db_dump program.

* Wed Oct 27 2010 Richard Jones <rjones@redhat.com> - 1:1.5.24-2
- Attempt to run tests.

* Wed Oct 27 2010 Richard Jones <rjones@redhat.com> - 1:1.5.24-1
- New upstream development version 1.5.24.

* Sat Oct 23 2010 Richard Jones <rjones@redhat.com> - 1:1.5.23-1
- Fix for libguestfs: missing disk format specifier when adding a disk
  (RHBZ#642934, CVE-2010-3851).

* Tue Oct 19 2010 Richard Jones <rjones@redhat.com> - 1:1.5.22-1
- New upstream development version 1.5.22.

* Sat Oct  9 2010 Richard Jones <rjones@redhat.com> - 1:1.5.21-2
- guestfish no longer requires virt-inspector.

* Fri Oct  1 2010 Richard Jones <rjones@redhat.com> - 1:1.5.21-1
- New upstream development version 1.5.21.

* Sun Sep 26 2010 Richard Jones <rjones@redhat.com> - 1:1.5.20-1
- New upstream development version 1.5.20.

* Wed Sep 22 2010 Richard Jones <rjones@redhat.com> - 1:1.5.18-1
- New upstream development version 1.5.18.
- Note that guestfish '-a' and '-d' options were broken in 1.5.17, so
  upgrading to this version is highly recommended.

* Tue Sep 21 2010 Richard Jones <rjones@redhat.com> - 1:1.5.17-1
- New upstream development version 1.5.17.

* Wed Sep 15 2010 Richard Jones <rjones@redhat.com> - 1:1.5.16-1
- New upstream development version 1.5.16.

* Wed Sep 15 2010 Richard Jones <rjones@redhat.com> - 1:1.5.15-1
- New upstream development version 1.5.15.

* Tue Sep 14 2010 Richard Jones <rjones@redhat.com> - 1:1.5.14-1
- New upstream development version 1.5.14.

* Mon Sep 13 2010 Richard Jones <rjones@redhat.com> - 1:1.5.13-1
- New upstream version 1.5.13.
- Removed the patch workaround for RHBZ#630583.  The same workaround
  is now upstream (the bug is not fixed).

* Sat Sep 11 2010 Richard Jones <rjones@redhat.com> - 1:1.5.12-1
- New upstream version 1.5.12.

* Fri Sep 10 2010 Richard Jones <rjones@redhat.com> - 1:1.5.11-1
- New upstream version 1.5.11.
- Note: fixes a serious bug in guestfish 'copy-out' command.

* Thu Sep  9 2010 Richard Jones <rjones@redhat.com> - 1:1.5.10-1
- New upstream version 1.5.10.

* Wed Sep  8 2010 Richard Jones <rjones@redhat.com> - 1:1.5.9-2
- Disable tests, still failing because of RHBZ#630777.

* Wed Sep  8 2010 Richard Jones <rjones@redhat.com> - 1:1.5.9-1
- New upstream version 1.5.9.

* Mon Sep  6 2010 Richard Jones <rjones@redhat.com> - 1:1.5.8-2
- Add patch to work around RHBZ#630583 and reenable tests.

* Sat Sep  4 2010 Richard Jones <rjones@redhat.com> - 1:1.5.8-1
- New upstream version 1.5.8.
- Add BR po4a for translations of man pages.
- Add PHP bindings.
- Remove partially-translated Japanese webpages.

* Wed Sep  1 2010 Richard Jones <rjones@redhat.com> - 1:1.5.7-1
- New upstream version 1.5.7.
- 'debug' command is enabled by default now.

* Fri Aug 27 2010 Richard Jones <rjones@redhat.com> - 1:1.5.6-1
- New upstream version 1.5.6.

* Fri Aug 27 2010 Richard Jones <rjones@redhat.com> - 1:1.5.5-2
- Use bug-fixed febootstrap 2.9.

* Thu Aug 26 2010 Richard Jones <rjones@redhat.com> - 1:1.5.5-1
- New upstream version 1.5.5.

* Tue Aug 24 2010 Richard Jones <rjones@redhat.com> - 1:1.5.4-2
- Disable tests again, because the Rawhide kernel still won't boot.

* Tue Aug 24 2010 Richard Jones <rjones@redhat.com> - 1:1.5.4-1
- New upstream development version 1.5.4.
- Now requires febootstrap >= 2.8 and qemu >= 0.12.
- Re-enable tests because RHBZ#624854 is supposed to be fixed.
- Upstream Source URL has changed.

* Wed Aug 18 2010 Richard Jones <rjones@redhat.com> - 1:1.5.3-2
- Disable tests because of RHBZ#624854.

* Tue Aug 17 2010 Richard Jones <rjones@redhat.com> - 1:1.5.3-1
- New upstream development version 1.5.3.

* Wed Aug 11 2010 Richard Jones <rjones@redhat.com> - 1:1.5.2-6
- Bump and rebuild.

* Thu Aug 05 2010 Richard Jones - 1:1.5.2-5
- Bump and rebuild.

* Fri Jul 23 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 23 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.2-2
- New upstream development version 1.5.2.
- +BuildRequires: cryptsetup-luks.

* Wed Jul 21 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.1-1
- New upstream development version 1.5.1.

* Tue Jul 20 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.0-7
- Requires binutils (RHBZ#616437).

* Mon Jul 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.0-6
- Fix libguestfs-find-requires.sh for new location of hostfiles (RHBZ#615946).

* Thu Jul  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.0-5
- Include RELEASE-NOTES in devel package.

* Thu Jul  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.0-4
- New development branch 1.5.0.
- Remove two upstream patches.
- Work around permanently broken test-getlogin_r Gnulib test.

* Mon Jun 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.21-4
- Explicitly depend on e2fsprogs.
- Add patch to add e2fsprogs to the appliance.
- Add patch to fix GFS kernel module problem.

* Fri Jun 25 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:1.3.21-2
- Rebuild

* Wed Jun 16 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.21-1
- New upstream version 1.3.21.

* Tue Jun  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.20-1
- New upstream version 1.3.20.
- Since upstream commit a043b6854a0c4 we don't need to run make install
  twice.

* Fri Jun  4 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.19-1
- New upstream version 1.3.19.

* Wed Jun  2 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.18-1
- New upstream version 1.3.18.

* Thu May 27 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.17-1
- New upstream version 1.3.17.
- Change repo name to 'fedora-14'.

* Wed May 26 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.16-6
- Co-own bash_completion.d directory.

* Tue May 25 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.16-4
- New upstream version 1.3.16.
- Add guestfish bash tab completion script.

* Mon May 24 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.14-1
- New upstream version 1.3.14.

* Sun May 16 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.13-1
- New upstream version 1.3.13.
- Add BUGS to documentation.
- Force update of hivex dependency to 1.2.2 since it contains
  important registry import fixes.
- Remove patch1, now upstream.

* Fri May 14 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.12-3
- Backport supermin build fix from upstream.
- Further changes required for new layout of supermin appliance.

* Fri May 14 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.12-1
- New upstream version 1.3.12.
- febootstrap >= 2.7 is required at compile time and at runtime (at runtime
  because of the new febootstrap-supermin-helper).
- Bugs fixed: 591155 591250 576879 591142 588651 507810 521674 559963 516096.

* Sat May  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.11-1
- New upstream version 1.3.11.

* Fri May  7 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.10-2
- New upstream version 1.3.10.

* Thu May 06 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.9-2
- Bump and rebuild against updated libconfig

* Fri Apr 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.9-1
- New upstream version 1.3.9.

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.3.8-2
- Mass rebuild with perl-5.12.0

* Tue Apr 27 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.8-1
- New upstream version 1.3.8.

* Fri Apr 23 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.7-1
- New upstream version 1.3.7.
- NOTE: fixes a segfault in guestfish 1.3.6 when using the -a option.

* Thu Apr 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.6-1
- New upstream version 1.3.6.

* Mon Apr 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.5-1
- New upstream version 1.3.5.

* Sat Apr 17 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.4-1
- New upstream version 1.3.4.

* Sun Apr 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.3-1
- New upstream version 1.3.3.
- New virt-resize option --LV-expand.
- New API: lvresize-free.
- Fixes RHBZ#581501.

* Sun Apr 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.2-3
- Disable checksum-device test.

* Sat Apr 10 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.2-2
- Bump and rebuild.

* Sat Apr 10 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.2-1
- New upstream version 1.3.2.
- New APIs: checksum-device, part-del, part-get-bootable, part-get-mbr-id,
  part-set-mbr-id, vgscan, ntfsresize, txz-in, txz-out.
- Enhanced/fixed virt-resize tool.
- Enhanced virt-list-partitions tool.
- Fixes: 580016, 580650, 579155, 580556.

* Sat Apr 10 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.1-4
- Bump and rebuild.

* Thu Apr  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.1-3
- Runtime requires should only be on libguestfs-tools subpackage.

* Thu Apr  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.1-2
- Missing BR on qemu-img package.

* Thu Apr  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.1-1
- New upstream version 1.3.1.
- For explanation of apparently large version jump, see:
  https://www.redhat.com/archives/libguestfs/2010-April/msg00057.html
- New tool: virt-make-fs.
- New API: guestfs_zero_device.
- Fixes RHBZ#580246 (tar-in command hangs if uploading more than
  available space)
- Fixes RHBZ#579664 (guestfish doesn't report error when there is not
  enough space for image allocation)
- +BR perl-String-ShellQuote (for virt-make-fs).

* Tue Mar 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.89-1
- New upstream version 1.0.89.
- Improved version of virt-win-reg.
- Many smaller bugfixes.
- Requires hivex >= 1.2.1.
- Remove TERM=dumb patch which is now upstream.

* Tue Mar 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.88-7
- Backport of TERM=dumb patch from upstream.
- Workaround failure caused by RHBZ#575734.
- Workaround unknown failure of test_swapon_label_0.

* Tue Mar 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.88-5
- Attempted workaround for RHBZ#563103, so we can reenable tests.

* Fri Mar 26 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.88-2
- Remember to check in the new sources.

* Fri Mar 26 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.88-1
- New upstream version 1.0.88.
- Mainly small bugfixes.
- Update Spanish translation of libguestfs (RHBZ#576876).
- Use ext4 dev tools on RHEL 5 (RHBZ#576688).
- Add support for minix filesystem (RHBZ#576689).

* Fri Mar 26 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.87-2
- Add vim-minimal to BR, it is now required by the appliance.

* Tue Mar 23 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.87-1
- New upstream version 1.0.87.
- New tools: virt-resize and virt-list-partitions.
- New APIs: guestfs_copy_size; APIs for querying the relationship between
  LVM objects.
- Add vim to the virt-rescue appliance.

* Fri Mar 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.86-1
- New upstream version 1.0.86.
- libguestfs-supermin-helper rewritten in C (from shell), reduces
  appliance boot time by 2-3 seconds.
- Fix parsing of integers in guestfish on 32 bit platforms (RHBZ#569757
  and RHBZ#567567).
- Enhance virt-inspector output for Windows guests.
- Add product_name field to virt-inspector output for all guests.
- Weaken dependencies on libntfs-3g.so, don't include SONAME in dep.
- Remove false dependency on libply (plymouth libraries).
- Spanish translation (RHBZ#570181).
- Fix bash regexp quoting bug.

* Fri Mar 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-4
- Bump and rebuild.

* Thu Mar 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-3
- Bump and rebuild.

* Sat Mar 06 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-2
- Bump and rebuild.

* Mon Mar  1 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-1
- New upstream version 1.0.85.
- Remove hivex, now a separate upstream project and package.
- Remove supermin quoting patch, now upstream.

* Mon Mar  1 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-6
- Fix quoting in supermin-split script (RHBZ#566511).
- Don't include bogus './builddir' entries in supermin hostfiles
  (RHBZ#566512).

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-4
- Don't include generator.ml in rpm.  It's 400K and almost no one will need it.
- Add comments to spec file about how repo building works.
- Whitespace changes in the spec file.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-3
- Bump and rebuild.

* Tue Feb 16 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-2
- Bump and rebuild.

* Fri Feb 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-1
- New upstream version 1.0.84.

* Fri Feb 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.83-8
- Bump and rebuild.

* Thu Feb 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-7
- Disable tests.  These fail in Koji (on RHEL 5 kernel) because of a
  bug in preadv/pwritev emulation in glibc (RHBZ#563103).

* Tue Feb  9 2010 Matthew Booth <mbooth@redhat.com> - 1.0.83-6
- Change buildnonet to buildnet
- Allow buildnet, mirror, updates, virtio and runtests to be configured by user
  macros.

* Mon Feb  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-5
- libguestfs-tools should require perl-XML-Writer (RHBZ#562858).

* Mon Feb  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-4
- Use virtio for block device access (RHBZ#509383 is fixed).

* Fri Feb  5 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-3
- Rebuild: possible timing-related build problem in Koji.

* Fri Feb  5 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-2
- New upstream release 1.0.83.
- This release fixes:
  Add Marathi translations (RHBZ#561671).
  Polish translations (RHBZ#502533).
  Add Gujarti translations (Sweta Kothari) (RHBZ#560918).
  Update Oriya translations (thanks Manoj Kumar Giri) (RHBZ#559498).
  Set locale in C programs so l10n works (RHBZ#559962).
  Add Tamil translation (RHBZ#559877) (thanks to I.Felix)
  Update Punjabi translation (RHBZ#559480) (thanks Jaswinder Singh)
- There are significant fixes to hive file handling.
- Add hivexsh and manual page.
- Remove two patches, now upstream.

* Sun Jan 31 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.82-7
- Bump and rebuild.

* Fri Jan 29 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.82-6
- Backport a better fix for RHBZ557655 test from upstream.
- Backport fix for unreadable yum.log from upstream.

* Thu Jan 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.82-3
- Backport RHBZ557655 test fix from upstream.

* Thu Jan 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.82-1
- New upstream version 1.0.82.  This includes the two patches
  we were carrying, so those are now removed.
- This release fixes:
  RHBZ#559498 (Oriya translation).
  RHBZ#559480 (Punjabi translation).
  RHBZ#558593 (Should prevent corruption by multilib).
  RHBZ#559237 (Telugu translation).
  RHBZ#557655 (Use xstrtol/xstrtoll to parse integers in guestfish).
  RHBZ#557195 (Missing crc kernel modules for recent Linux).
- In addition this contains numerous fixes to the hivex library
  for parsing Windows Registry files, making hivex* and virt-win-reg
  more robust.
- New API call 'filesize'.

* Thu Jan 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-8
- Backport special handling of libgcc_s.so.
- Backport unreadable files patch from RHEL 6 / upstream.

* Fri Jan 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-5
- Require febootstrap >= 2.6 (RHBZ#557262).

* Thu Jan 21 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-4
- Rebuild for unannounced soname bump (libntfs-3g.so).

* Fri Jan 15 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-3
- Rebuild for unannounced soname bump (libplybootsplash.so).

* Thu Jan 14 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-2
- Rebuild for broken dependency (iptables soname bump).

* Wed Jan 13 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-1
- New upstream version 1.0.81.
- Remove two upstream patches.
- virt-inspector: Make RPM application data more specific (RHBZ#552718).

* Tue Jan 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-14
- Reenable tests because RHBZ#553689 is fixed.

* Tue Jan 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-13
- Rebuild because of libparted soname bump (1.9 -> 2.1).

* Fri Jan  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-12
- qemu in Rawhide is totally broken (RHBZ#553689).  Disable tests.

* Thu Jan  7 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-11
- Remove gfs-utils (deprecated and removed from Fedora 13 by the
  upstream Cluster Suite developers).
- Include patch to fix regression in qemu -serial stdio option.

* Tue Dec 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-10
- Remove some debugging statements which were left in the requires
  script by accident.

* Mon Dec 21 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-9
- Generate additional requires for supermin (RHBZ#547496).

* Fri Dec 18 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-3
- Work around udevsettle command problem (RHBZ#548121).
- Enable tests.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-2
- Disable tests because of RHBZ#548121.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-1
- New upstream release 1.0.80.
- New Polish translations (RHBZ#502533).
- Give a meaningful error if no usable kernels are found (RHBZ#539746).
- New tool: virt-list-filesystems

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1:1.0.79-3
- rebuild against perl 5.10.1

* Wed Nov 18 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.79-2
- New upstream release 1.0.79.
- Adds FUSE test script and multiple fixes for FUSE (RHBZ#538069).
- Fix virt-df in Xen (RHBZ#538041).
- Improve speed of supermin appliance.
- Disable FUSE-related tests because Koji doesn't currently allow them.
  fuse: device not found, try 'modprobe fuse' first

* Tue Nov 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.78-2
- New upstream release 1.0.78.
- Many more filesystem types supported by this release - add them
  as dependencies.

* Tue Nov  3 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.77-1
- New upstream release 1.0.77.
- Support for mounting guest in host using FUSE (guestmount command).
- hivex*(1) man pages should be in main package, not -devel, since
  they are user commands.
- libguestfs-tools: Fix "self-obsoletion" issue raised by rpmlint.
- perl: Remove bogus script Sys/bindtests.pl.

* Thu Oct 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.75-2
- New upstream release 1.0.75.
- New library: libhivex.
- New tools: virt-win-reg, hivexml, hivexget.
- Don't require chntpw.
- Add BR libxml2-devel, accidentally omitted before.

* Tue Oct 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.74-1
- New upstream release 1.0.74.
- New API call: guestfs_find0.
- New tools: virt-ls, virt-tar.

* Wed Oct 14 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.73-1
- New upstream release 1.0.73.
- OCaml library now depends on xml-light.
- Deal with installed documentation.

* Tue Sep 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.72-2
- Force rebuild.

* Wed Sep 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.72-1
- New upstream release 1.0.72.
- New tools: virt-edit, virt-rescue.
- Combine virt-cat, virt-df, virt-edit, virt-inspector and virt-rescue
  into a single package called libguestfs-tools.

* Tue Sep 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.71-2
- New upstream release 1.0.71.

* Fri Sep 18 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.70-2
- Perl bindings require perl-XML-XPath (fixed RHBZ#523547).

* Tue Sep 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.70-1
- New upstream release 1.0.70.
- Fixes build problem related to old version of GNU gettext.

* Tue Sep 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.69-1
- New upstream release 1.0.69.
- Reenable the tests (because RHBZ#516543 is supposed to be fixed).
- New main loop code should fix RHBZ#501888, RHBZ#504418.
- Add waitpid along guestfs_close path (fixes RHBZ#518747).

* Wed Aug 19 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.68-2
- New upstream release 1.0.68.
- BR genisoimage.

* Thu Aug 13 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.67-2
- New upstream release 1.0.67.

* Fri Aug  7 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.66-5
- Set network interface to ne2k_pci (workaround for RHBZ#516022).
- Rerun autoconf because patch touches configure script.

* Thu Aug  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.66-1
- New upstream release 1.0.66.

* Wed Jul 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.65-1
- New upstream release 1.0.65.
- Add Obsoletes for virt-df2 (RHBZ#514309).
- Disable tests because of ongoing TCG problems with newest qemu in Rawhide.

* Thu Jul 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.64-3
- RHBZ#513249 bug in qemu is now fixed, so try to rebuild and run tests.
- However RHBZ#503236 still prevents us from testing on i386.

* Thu Jul 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.64-1
- New upstream release 1.0.64.
- New tool 'libguestfs-test-tool'.

* Wed Jul 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.61-1
- New upstream release 1.0.61.
- New tool / subpackage 'virt-cat'.
- New BR perl-libintl.

* Wed Jul 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.60-2
- Fix runtime Requires so they use epoch correctly.

* Tue Jul 14 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.60-1
- New upstream release 1.0.60.

* Fri Jul 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.58-2
- New upstream release 1.0.58.

* Fri Jul 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.57-1
- New upstream release 1.0.57.
- New tool virt-df (obsoletes existing package with this name).
- RHBZ#507066 may be fixed, so reenable tests.

* Tue Jul  7 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.56-2
- New upstream release 1.0.56.
- Don't rerun generator.

* Thu Jul  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.55-1
- New upstream release 1.0.55.
- New manual page libguestfs(3).

* Mon Jun 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.54-2
- New upstream release 1.0.54.
- +BR perl-XML-Writer.

* Wed Jun 24 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.53-1
- New upstream release 1.0.53.
- Disable all tests (because of RHBZ#507066).

* Wed Jun 24 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.52-1
- New upstream release 1.0.52.

* Mon Jun 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.51-1
- New upstream release 1.0.51.
- Removed patches which are now upstream.

* Sat Jun 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.49-5
- Remove workaround for RHBZ#507007, since bug is now fixed.
- Pull in upstream patch to fix pclose checking
  (testing as possible fix for RHBZ#507066).
- Pull in upstream patch to check waitpid return values
  (testing as possible fix for RHBZ#507066).

* Fri Jun 19 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.49-2
- New upstream release 1.0.49.
- Add workaround for RHBZ#507007.

* Tue Jun 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.48-2
- Accidentally omitted the supermin image from previous version.

* Tue Jun 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.48-1
- New upstream release 1.0.48.
- Should fix all the brokenness from 1.0.47.
- Requires febootstrap >= 2.3.

* Mon Jun 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.47-2
- New upstream release 1.0.47.
- Enable experimental supermin appliance build.
- Fix path to appliance.

* Fri Jun 12 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.45-2
- New upstream release 1.0.45.

* Wed Jun 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.44-2
- Disable ppc/ppc64 tests again because of RHBZ#505109.

* Wed Jun 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.44-1
- New upstream version 1.0.44.
- Try enabling tests on ppc & ppc64 since it looks like the bug(s?)
  in qemu which might have caused them to fail have been fixed.

* Tue Jun  9 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.43-1
- New upstream version 1.0.43.
- New upstream URL.
- Requires chntpw program.

* Sat Jun  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.42-1
- New upstream version 1.0.42.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.41-1
- New upstream version 1.0.41.
- Fixes a number of regressions in RHBZ#503169.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.40-1
- New upstream version 1.0.40.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.39-1
- New upstream version 1.0.39.
- Fixes:
  . libguestfs /dev is too sparse for kernel installation/upgrade (RHBZ#503169)
  . OCaml bindings build failure (RHBZ#502309)

* Tue Jun  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.38-2
- Disable tests on ix86 because of RHBZ#503236.

* Tue Jun  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.38-1
- New upstream version 1.0.38.

* Fri May 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.37-1
- New upstream version 1.0.37.
- Fixes:
  . "mkdir-p" should not throw errors on preexisting directories (RHBZ#503133)
  . cramfs and squashfs modules should be available in libguestfs appliances
      (RHBZ#503135)

* Thu May 28 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.36-2
- New upstream version 1.0.36.
- Rerun the generator in prep section.

* Thu May 28 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.35-1
- New upstream version 1.0.35.
- Fixes multiple bugs in bindings parameters (RHBZ#501892).

* Wed May 27 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.34-1
- New upstream version 1.0.34.

* Wed May 27 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.33-1
- New upstream version 1.0.33.
- --with-java-home option is no longer required.
- Upstream contains potential fixes for:
    501878 built-in commands like 'alloc' and 'help' don't autocomplete
    501883 javadoc messed up in libguestfs java documentation
    501885 Doesn't detect missing Java, --with-java-home=no should not be needed
    502533 Polish translation of libguestfs
    n/a    Allow more ext filesystem kmods (Charles Duffy)

* Tue May 26 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.32-2
- New upstream version 1.0.32.
- Use %%find_lang macro.

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.31-1
- Rebuild for OCaml 3.11.1.
- New upstream version 1.0.31.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.30-1
- New upstream version 1.0.30.  Now includes test-bootbootboot.sh script.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.29-3
- New upstream version 1.0.29 (fixes RHBZ#502007 RHBZ#502018).
- This should allow us to enable tests for i386 and x86-64.
- Added test-bootbootboot.sh script which was missed from 1.0.29 tarball.
- Pass kernel noapic flag to workaround RHBZ#502058.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.28-1
- New upstream version 1.0.28.  Nothing has visibly changed, but
  the source has been gettextized and we want to check that doesn't
  break anything.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.27-3
- Change requirement from qemu -> qemu-kvm (RHBZ#501761).

* Tue May 19 2009 Richard Jones <rjones@redhat.com> - 1.0.27-2
- New upstream version 1.0.27.

* Mon May 18 2009 Richard Jones <rjones@redhat.com> - 1.0.26-6
- Experimentally try to reenable ppc and ppc64 builds.
- Note BZ numbers which are causing tests to fail.

* Mon May 18 2009 Richard Jones <rjones@redhat.com> - 1.0.26-1
- New upstream version 1.0.26.

* Tue May 12 2009 Richard Jones <rjones@redhat.com> - 1.0.25-4
- New upstream version 1.0.25.
- Enable debugging when running the tests.
- Disable tests - don't work correctly in Koji.

* Tue May 12 2009 Richard Jones <rjones@redhat.com> - 1.0.24-1
- New upstream version 1.0.24.
- BRs glibc-static for the new command tests.
- Enable tests.

* Mon May 11 2009 Richard Jones <rjones@redhat.com> - 1.0.23-2
- New upstream version 1.0.23.
- Don't try to use updates during build.

* Fri May  8 2009 Richard Jones <rjones@redhat.com> - 1.0.21-3
- New upstream version 1.0.21.

* Thu May  7 2009 Richard Jones <rjones@redhat.com> - 1.0.20-2
- New upstream version 1.0.20.

* Thu May  7 2009 Richard Jones <rjones@redhat.com> - 1.0.19-1
- New upstream version 1.0.19.

* Tue Apr 28 2009 Richard Jones <rjones@redhat.com> - 1.0.15-1
- New upstream version 1.0.15.

* Fri Apr 24 2009 Richard Jones <rjones@redhat.com> - 1.0.12-1
- New upstream version 1.0.12.

* Wed Apr 22 2009 Richard Jones <rjones@redhat.com> - 1.0.6-1
- New upstream version 1.0.6.

* Mon Apr 20 2009 Richard Jones <rjones@redhat.com> - 1.0.2-1
- New upstream version 1.0.2.

* Thu Apr 16 2009 Richard Jones <rjones@redhat.com> - 0.9.9-12
- Multiple fixes to get it to scratch build in Koji.

* Sat Apr  4 2009 Richard Jones <rjones@redhat.com> - 0.9.9-1
- Initial build.
