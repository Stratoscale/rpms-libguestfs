# Enable to build w/o network.
%global buildnonet 1

Summary:     Access and modify virtual machine disk images
Name:        libguestfs
Version:     1.0.61
Release:     2%{?dist}
License:     LGPLv2+
Group:       Development/Libraries
URL:         http://libguestfs.org/
Source0:     http://libguestfs.org/download/%{name}-%{version}.tar.gz
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root

# Currently fails on PPC because:
# "No Package Found for kernel"
ExclusiveArch: %{ix86} x86_64

# Basic build requirements:
BuildRequires: /usr/bin/pod2man
BuildRequires: /usr/bin/pod2text
BuildRequires: febootstrap >= 2.3
#BuildRequires: augeas-devel >= 0.5.0
BuildRequires: readline-devel
BuildRequires: squashfs-tools
%ifarch %{ix86} x86_64
BuildRequires: qemu-system-x86 >= 0.10.5
%endif
%ifarch ppc ppc64
BuildRequires: qemu-system-ppc >= 0.10.5
%endif
BuildRequires: createrepo

# This is only needed for RHEL 5 because readline-devel doesn't
# properly depend on it, but doesn't do any harm on other platforms:
BuildRequires: ncurses-devel

# Build requirements for the appliance (see 'make.sh.in' in the source):
BuildRequires: kernel, bash, coreutils, lvm2
BuildRequires: MAKEDEV, net-tools, file
BuildRequires: module-init-tools, procps, strace, iputils
BuildRequires: dosfstools, lsof, scrub
# Not supported in EPEL yet: ntfs-3g util-linux-ng zerofree
# Not working: augeas-libs
%ifarch %{ix86} x86_64
BuildRequires: grub, ntfsprogs
%endif

# Must match the above set of BuildRequires exactly!
Requires:      kernel, bash, coreutils, lvm2
Requires:      MAKEDEV, net-tools, file
Requires:      module-init-tools, procps, strace, iputils
Requires:      dosfstools, lsof, scrub
# Not supported in EPEL yet: ntfs-3g util-linux-ng zerofree
# Not working: augeas-libs
%ifarch %{ix86} x86_64
Requires:      grub, ntfsprogs
%endif

# These are only required if you want to build the bindings for
# different languages:
BuildRequires: ocaml
BuildRequires: ocaml-findlib-devel
#BuildRequires: perl-devel
#BuildRequires: perl-Test-Simple
BuildRequires: perl-Test-Pod
BuildRequires: perl-Test-Pod-Coverage
#BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: perl-XML-Writer
#BuildRequires: perl-libintl
BuildRequires: python-devel
BuildRequires: ruby-devel
BuildRequires: rubygem-rake
BuildRequires: java >= 1.5.0
BuildRequires: jpackage-utils
BuildRequires: java-devel

# For virt-inspector:
#BuildRequires: perl-Sys-Virt

# Runtime requires:
%ifarch %{ix86} x86_64
Requires:      qemu-system-x86 >= 0.10.5
%endif
%ifarch ppc ppc64
Requires:      qemu-system-ppc >= 0.10.5
%endif

# For virt-inspector --windows-registry option.
Requires:      chntpw >= 0.99.6-8


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
in the context of the guest.  Also you can access filesystems over FTP.

Libguestfs is a library that can be linked with C and C++ management
programs.

See also the 'guestfish' package for shell scripting and command line
access.

For Perl bindings, see 'perl-libguestfs'.

For OCaml bindings, see 'ocaml-libguestfs-devel'.

For Python bindings, see 'python-libguestfs'.

For Ruby bindings, see 'ruby-libguestfs'.

For Java bindings, see 'libguestfs-java-devel'.


%package devel
Summary:     Development tools and libraries for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{epoch}:%{version}-%{release}
Requires:    pkgconfig


%description devel
%{name}-devel contains development tools and libraries
for %{name}.


%package -n guestfish
Summary:     Shell for accessing and modifying virtual machine disk images
Group:       Development/Tools
License:     GPLv2+
Requires:    %{name} = %{epoch}:%{version}-%{release}
Requires:    /usr/bin/pod2text
Requires:    virt-inspector


%description -n guestfish
Guestfish is the Filesystem Interactive SHell, for accessing and
modifying virtual machine disk images from the command line and shell
scripts.


#%package -n virt-inspector
#Summary:     Display OS version, kernel, drivers, etc in a virtual machine
#Group:       Development/Tools
#License:     GPLv2+
#Requires:    %{name} = %{epoch}:%{version}-%{release}
#Requires:    guestfish
#Requires:    perl-Sys-Virt
#
#
#%description -n virt-inspector
#Virt-inspector examines a virtual machine and tries to determine the
#version of the OS, the kernel version, what drivers are installed,
#whether the virtual machine is fully virtualized (FV) or
#para-virtualized (PV), what applications are installed and more.


#%package -n virt-df
#Summary:     Display free space on virtual filesystems
#Group:       Development/Tools
#License:     GPLv2+
#Requires:    %{name} = %{epoch}:%{version}-%{release}
#Requires:    perl-Sys-Virt
#
#
#%description -n virt-df
#"virt-df" is a command line tool to display free space on virtual
#machine filesystems.  Unlike other tools, it doesn’t just display the
#amount of space allocated to a virtual machine, but can look inside
#the virtual machine to see how much space is really being used.
#
#It is like the df(1) command, but for virtual machines, except that it
#also works for Windows virtual machines.


#%package -n virt-cat
#Summary:     Display a file in a virtual machine
#Group:       Development/Tools
#License:     GPLv2+
#Requires:    %{name} = %{epoch}:%{version}-%{release}
#Requires:    perl-Sys-Virt
#
#
#%description -n virt-cat
#"virt-cat" is a command line tool to display the contents
#of a file in a virtual machine.


%package -n ocaml-%{name}
Summary:     OCaml bindings for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{epoch}:%{version}-%{release}


%description -n ocaml-%{name}
ocaml-%{name} contains OCaml bindings for %{name}.

This is for toplevel and scripting access only.  To compile OCaml
programs which use %{name} you will also need ocaml-%{name}-devel.


%package -n ocaml-%{name}-devel
Summary:     OCaml bindings for %{name}
Group:       Development/Libraries
Requires:    ocaml-%{name} = %{epoch}:%{version}-%{release}


%description -n ocaml-%{name}-devel
ocaml-%{name}-devel contains development libraries
required to use the OCaml bindings for %{name}.


%package -n perl-%{name}
Summary:     Perl bindings for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{epoch}:%{version}-%{release}
Requires:    perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description -n perl-%{name}
perl-%{name} contains Perl bindings for %{name}.


%package -n python-%{name}
Summary:     Python bindings for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{epoch}:%{version}-%{release}

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description -n python-%{name}
python-%{name} contains Python bindings for %{name}.


%package -n ruby-%{name}
Summary:     Ruby bindings for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{epoch}:%{version}-%{release}
Requires:    ruby(abi) = 1.8
Provides:    ruby(guestfs) = %{version}

%{!?ruby_sitelib: %define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}
%{!?ruby_sitearch: %define ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

%description -n ruby-%{name}
ruby-%{name} contains Ruby bindings for %{name}.


%package java
Summary:     Java bindings for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{epoch}:%{version}-%{release}
Requires:    java >= 1.5.0
Requires:    jpackage-utils

%description java
%{name}-java contains Java bindings for %{name}.

If you want to develop software in Java which uses %{name}, then
you will also need %{name}-java-devel.


%package java-devel
Summary:     Java development package for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{epoch}:%{version}-%{release}
Requires:    %{name}-java = %{epoch}:%{version}-%{release}

%description java-devel
%{name}-java-devel contains the tools for developing Java software
using %{name}.

See also %{name}-javadoc.


%package javadoc
Summary:     Java documentation for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{epoch}:%{version}-%{release}
Requires:    %{name}-java = %{epoch}:%{version}-%{release}
Requires:    jpackage-utils

%description javadoc
%{name}-javadoc contains the Java documentation for %{name}.


%prep
%setup -q

mkdir -p daemon/m4


%build
%if %{buildnonet}
mkdir repo
find /var/cache/yum/ -type f -name '*.rpm' -print0 | xargs -0 cp -t repo
createrepo repo
ls -l repo
%define extra --with-mirror=file://$(pwd)/repo --with-repo=epel-5 --with-updates=none
%else
%define extra --with-mirror=http://mirror.centos.org/centos-5/5.3/os/%{_arch}/ --with-repo=centos-5 --with-updates=none
%endif

vmchannel_test=no \
./configure \
  --prefix=%{_prefix} --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --with-qemu="qemu-kvm qemu-system-%{_build_arch} qemu" \
  --enable-debug-command \
  --enable-supermin \
  %{extra}

# This ensures that /usr/sbin/chroot is on the path.  Not needed
# except for RHEL 5, it shouldn't do any harm on other platforms.
export PATH=/usr/sbin:$PATH

# 'INSTALLDIRS' ensures that perl libs are installed in the vendor dir
# not the site dir.
make INSTALLDIRS=vendor %{?_smp_mflags}


%check
# Enable debugging - very useful if a test does fail, although
# it produces masses of output in the build.log.
export LIBGUESTFS_DEBUG=1

# Workaround for BZ 502058.  This is needed sometimes (but not
# always) for EL-5.  We don't know why it only affects some boots.
export LIBGUESTFS_APPEND="noapic"

# Tests fail on i386.  We don't know why because plague doesn't let us
# see the logs (the tests hang rather than failing completely).

%ifarch x86_64
make check
%endif


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Delete the ordinary appliance, leaving just the supermin appliance.
rm $RPM_BUILD_ROOT%{_libdir}/guestfs/vmlinuz.*
mkdir keep
mv $RPM_BUILD_ROOT%{_libdir}/guestfs/initramfs.*.supermin.img keep
rm $RPM_BUILD_ROOT%{_libdir}/guestfs/initramfs.*.img
mv keep/* $RPM_BUILD_ROOT%{_libdir}/guestfs/
rmdir keep

# Delete static libraries, libtool files.
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs.a
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs.la

# Clean up the examples/ directory which will get installed in %doc.
# Note we can't delete the original examples/Makefile because that
# will be needed by the check section later in the RPM build.
cp -a examples ex
pushd ex
make clean
rm Makefile*
rm -rf .deps .libs
popd

# Same for ocaml/examples.
cp -a ocaml/examples ocaml/ex
pushd ocaml/ex
make clean
rm Makefile*
popd

find $RPM_BUILD_ROOT -name perllocal.pod -delete
find $RPM_BUILD_ROOT -name .packlist -delete
find $RPM_BUILD_ROOT -name '*.bs' -delete

rm $RPM_BUILD_ROOT%{python_sitearch}/libguestfsmod.a
rm $RPM_BUILD_ROOT%{python_sitearch}/libguestfsmod.la

if [ "$RPM_BUILD_ROOT%{python_sitearch}" != "$RPM_BUILD_ROOT%{python_sitelib}" ]; then
   mkdir -p $RPM_BUILD_ROOT%{python_sitelib}
   mv $RPM_BUILD_ROOT%{python_sitearch}/guestfs.py* \
     $RPM_BUILD_ROOT%{python_sitelib}/
fi

# Install ruby bindings by hand.
mkdir -p $RPM_BUILD_ROOT%{ruby_sitelib}
mkdir -p $RPM_BUILD_ROOT%{ruby_sitearch}
install -p -m0644 ruby/lib/guestfs.rb $RPM_BUILD_ROOT%{ruby_sitelib}
install -p -m0755 ruby/ext/guestfs/_guestfs.so $RPM_BUILD_ROOT%{ruby_sitearch}

# Remove static-linked Java bindings.
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs_jni.a
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs_jni.la

# Generator shouldn't be executable when we distribute it.
chmod -x src/generator.ml

# Find locale files.
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/libguestfs-supermin-helper
%{_libdir}/guestfs/
%{_libdir}/libguestfs.so.*


%files devel
%defattr(-,root,root,-)
%doc ChangeLog HACKING TODO README ex html/guestfs.3.html html/pod.css
%doc src/generator.ml
%{_libdir}/libguestfs.so
%{_mandir}/man3/guestfs.3*
%{_mandir}/man3/libguestfs.3*
%{_includedir}/guestfs.h
%{_includedir}/guestfs-actions.h
%{_includedir}/guestfs-structs.h
%{_libdir}/pkgconfig/libguestfs.pc


%files -n guestfish
%defattr(-,root,root,-)
%doc html/guestfish.1.html html/pod.css recipes/
%{_bindir}/guestfish
%{_mandir}/man1/guestfish.1*


#%files -n virt-inspector
#%defattr(-,root,root,-)
#%{_bindir}/virt-inspector
#%{_mandir}/man1/virt-inspector.1*


#%files -n virt-df
#%defattr(-,root,root,-)
#%{_bindir}/virt-df
#%{_mandir}/man1/virt-df.1*


#%files -n virt-cat
#%defattr(-,root,root,-)
#%{_bindir}/virt-cat
#%{_mandir}/man1/virt-cat.1*


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
%doc ocaml/ex
%{_libdir}/ocaml/guestfs/*.a
%{_libdir}/ocaml/guestfs/*.cmxa
%{_libdir}/ocaml/guestfs/*.cmx
%{_libdir}/ocaml/guestfs/*.mli


%files -n perl-%{name}
%defattr(-,root,root,-)
%doc perl/examples
%{perl_vendorarch}/*
%{_mandir}/man3/Sys::Guestfs.3pm*
%{_mandir}/man3/Sys::Guestfs::Lib.3pm*


%files -n python-%{name}
%defattr(-,root,root,-)
%doc README
%{python_sitearch}/*
%{python_sitelib}/*.py
%{python_sitelib}/*.pyc
%{python_sitelib}/*.pyo


%files -n ruby-%{name}
%defattr(-,root,root,-)
%doc README
%{ruby_sitelib}/guestfs.rb
%{ruby_sitearch}/_guestfs.so


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


%changelog
* Wed Jul 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.61-2
- New upstream release 1.0.61.
- New tool / subpackage 'virt-cat'.
- New BR perl-libintl (not enabled, because not in EPEL).

* Wed Jul 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.60-2
- Fix runtime Requires so they use epoch correctly.

* Tue Jul 14 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.60-1
- New upstream release 1.0.60.

* Fri Jul 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.58-2
- New upstream release 1.0.58.

* Fri Jul 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.57-2
- New upstream release 1.0.57.
- Workaround for RHBZ#502058.

* Tue Jul  7 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.56-1
- New upstream release 1.0.56.

* Thu Jul  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.55-1
- New upstream release 1.0.55.
- New manual page libguestfs(3).

* Mon Jun 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.54-2
- New upstream release 1.0.54.
- +BR perl-XML-Writer.

* Mon Jun 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.51-1
- New upstream release 1.0.51.
- Enable supermin appliance, backporting changes from devel branch.

* Thu Jun 11 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.44-1.el5.1
- Tests fail on i386 (impossible to debug because there are no
  log files available in plague), so disable tests on i386.
- Tests succeeded on x86-64, so leave enabled on this platform.

* Wed Jun 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.44-1
- New upstream version 1.0.44.
- This release is supposed to fix the testsuite under RHEL 5, so
  try enabling tests.

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

* Tue Jun  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.38-1
- New upstream version 1.0.38.

* Fri May 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.37-1
- New upstream version 1.0.37.
- Fixes:
  . "mkdir-p" should not throw errors on preexisting directories (RHBZ#503133)
  . cramfs and squashfs modules should be available in libguestfs appliances
      (RHBZ#503135)

* Thu May 28 2009 Richard Jones <rjones@redhat.com> - 1.0.35-1
- New upstream version 1.0.35.
- Disable tests, they took over 24 hours to run.

* Wed May 27 2009 Richard Jones <rjones@redhat.com> - 1.0.34-1.el5.3
- Fails to build on PPC.
- Fix missing Augeas dependency.

* Wed May 27 2009 Richard Jones <rjones@redhat.com> - 1.0.34-1
- Backport 1.0.34 from devel to EPEL.
- There should now be a working qemu in EPEL (0.10.5).

* Wed May 13 2009 Richard Jones <rjones@redhat.com> - 1.0.23-9
- Remove the runtime requires on non-existant package.  It'll just fail
  instead.

* Mon May 11 2009 Richard Jones <rjones@redhat.com> - 1.0.23-8
- New upstream version 1.0.23.
- Disable vmchannel test.
- Disable updates repo.
- Fix specfile for EPEL build.
- Correct yum location.
- Need _a_ version of qemu installed when installing.
- *.pyc and *.pyo files are present on x86_64.

* Fri May  8 2009 Richard Jones <rjones@redhat.com> - 1.0.21-2
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
