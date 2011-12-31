Name:           sanlock
Version:        1.8
Release:        2%{?dist}
Summary:        A shared disk lock manager

Group:          System Environment/Base
License:        GPLv2, GPLv2+, LGPLv2+
URL:            https://fedorahosted.org/sanlock/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch:  i686 x86_64
BuildRequires:  libblkid-devel libaio-devel python python-devel
Requires:       %{name}-lib = %{version}-%{release}
Source0:        https://fedorahosted.org/releases/s/a/sanlock/%{name}-%{version}.tar.gz

%description
sanlock uses disk paxos to manage leases on shared storage.
Hosts connected to a common SAN can use this to synchronize their
access to the shared disks.

%prep
%setup -q

%build
# upstream does not require configure
# upstream does not support _smp_mflags
CFLAGS=$RPM_OPT_FLAGS make -C wdmd
CFLAGS=$RPM_OPT_FLAGS make -C src
CFLAGS=$RPM_OPT_FLAGS make -C python

%install
rm -rf $RPM_BUILD_ROOT
make -C src \
        install LIBDIR=%{_libdir} \
        DESTDIR=$RPM_BUILD_ROOT
make -C wdmd \
        install LIBDIR=%{_libdir} \
        DESTDIR=$RPM_BUILD_ROOT
make -C python \
        install LIBDIR=%{_libdir} \
        DESTDIR=$RPM_BUILD_ROOT
install -D -m 755 init.d/sanlock $RPM_BUILD_ROOT/%{_initddir}/sanlock
install -D -m 755 init.d/wdmd $RPM_BUILD_ROOT/%{_initddir}/wdmd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/useradd -u 179 -c "sanlock" -s /sbin/nologin -r \
                  -d /var/run/sanlock sanlock 2> /dev/null || :

%post
/sbin/chkconfig --add sanlock
/sbin/chkconfig --add wdmd

%preun
if [ $1 = 0 ]; then
	/sbin/service sanlock stop > /dev/null 2>&1
	/sbin/service wdmd stop > /dev/null 2>&1
	/sbin/chkconfig --del sanlock
	/sbin/chkconfig --del wdmd
fi

%postun
#/sbin/service sanlock condrestart >/dev/null 2>&1 || :
#/sbin/service wdmd condrestart >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%{_initddir}/sanlock
%{_initddir}/wdmd
%{_sbindir}/sanlock
%{_sbindir}/wdmd
%{_mandir}/man8/wdmd*
%{_mandir}/man8/sanlock*

%package        lib
Summary:        A shared disk lock manager library
Group:          System Environment/Libraries

%description    lib
The %{name}-lib package contains the runtime libraries for sanlock,
a shared disk lock manager.
Hosts connected to a common SAN can use this to synchronize their
access to the shared disks.

%post lib -p /sbin/ldconfig

%postun lib -p /sbin/ldconfig

%files          lib
%defattr(-,root,root,-)
%{_libdir}/libsanlock.so.*
%{_libdir}/libsanlock_client.so.*
%{_libdir}/libwdmd.so.*

%package        python
Summary:        Python bindings for the sanlock library
Group:          Development/Libraries
Requires:       %{name}-lib = %{version}-%{release}

%description    python
The %{name}-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the sanlock library.

%files          python
%defattr(-,root,root,-)
%{python_sitearch}/Sanlock-1.0-py2.6.egg-info
%{python_sitearch}/sanlock.so

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-lib = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files          devel
%defattr(-,root,root,-)
%{_libdir}/libwdmd.so
%{_includedir}/wdmd.h
%{_libdir}/libsanlock.so
%{_libdir}/libsanlock_client.so
%{_includedir}/sanlock.h
%{_includedir}/sanlock_rv.h
%{_includedir}/sanlock_admin.h
%{_includedir}/sanlock_resource.h
%{_includedir}/sanlock_direct.h

%changelog
* Tue Sep 20 2011 David Teigland <teigland@redhat.com> - 1.8-2
- fix useradd command in spec file

* Fri Sep 16 2011 David Teigland <teigland@redhat.com> - 1.8-1
- Update to sanlock-1.8

* Sun Aug 07 2011 Chris Feist <cfeist@redhat.com> - 1.7-4
- Fix for minor file include issues

* Fri Aug 05 2011 David Teigland <teigland@redhat.com> - 1.7-3
- fix man page mode

* Fri Aug 05 2011 David Teigland <teigland@redhat.com> - 1.7-1
- Update to sanlock-1.7

* Fri Jul 08 2011 David Teigland <teigland@redhat.com> - 1.6-1
- Update to sanlock-1.6

* Thu Jun 30 2011 David Teigland <teigland@redhat.com> - 1.5-1
- Update to sanlock-1.5

* Tue Jun 21 2011 David Teigland <teigland@redhat.com> - 1.4-1
- Update to sanlock-1.4

* Fri Jun 10 2011 David Teigland <teigland@redhat.com> - 1.3-6
- fix python version, build i686 also

* Thu Jun 09 2011 David Teigland <teigland@redhat.com> - 1.3-5
- build exclusive x86_64, at least for now

* Thu Jun 09 2011 David Teigland <teigland@redhat.com> - 1.3-4
- build only x86_64, at least for now

* Thu Jun 09 2011 David Teigland <teigland@redhat.com> - 1.3-3
- fix libwdmd linking

* Thu Jun 09 2011 David Teigland <teigland@redhat.com> - 1.3-2
- shut up build warnings for wdmd and sanlock

* Thu Jun 09 2011 David Teigland <teigland@redhat.com> - 1.3-1
- Update to sanlock-1.3

* Mon May 09 2011 Chris Feist <cfeist@redhat.com> - 1.2.0-3
- Add python and python-devel to build requires

* Mon May 09 2011 Chris Feist <cfeist@redhat.com> - 1.2.0-1
- Use latest sources
- Sync .spec file

* Mon Apr  4 2011 Federico Simoncelli <fsimonce@redhat.com> - 1.1.0-3
- Add sanlock_admin.h header

* Fri Feb 18 2011 Chris Feist <cfeist@redhat.com> - 1.1.0-2
- Fixed install for wdmd

* Thu Feb 17 2011 Chris Feist <cfeist@redhat.com> - 1.1.0-1
- Updated to latest sources
- Now include wdmd

* Tue Feb 8 2011 Angus Salkeld <asalkeld@redhat.com> - 1.0-2
- SPEC: Add docs and make more consistent with the fedora template

* Mon Jan 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0-1
- first cut at rpm packaging
