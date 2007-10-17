%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Name:           bodhi
Version:        0.3.2
Release:        1%{?dist}
Summary:        A modular framework that facilitates publishing software updates
Group:          Applications/Internet
License:        GPLv2+
URL:            https://hosted.fedoraproject.org/projects/bodhi
Source0:        bodhi-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires: python-setuptools-devel

%description
Bodhi is a modular frameworkthat facilitates the process of publishing
updates for a software distribution.

%package client
Summary: Bodhi Client
Group: Applications/Internet
Requires: python-simplejson python-fedora

%description client 
Client tools for interacting with bodhi


%package server
Summary: A modular framework that facilitates publishing software updates
Group: Applications/Internet
Requires: TurboGears createrepo python-TurboMail intltool mash cvs python-fedora
# We need the --repofrompath option from yum-utils
Requires: yum-utils >= 1.1.7

%description server
Bodhi is a modular framework that facilitates the process of publishing
updates for a software distribution.

%prep
%setup -q


%build
%{__python} setup.py build --install-conf=%{_sysconfdir} \
        --install-data=%{_datadir}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --install-conf=%{_sysconfdir} \
    --install-data=%{_datadir} --root %{buildroot}
%{__install} -D bodhi/tools/bodhi-client.py $RPM_BUILD_ROOT/usr/bin/bodhi


%clean
rm -rf $RPM_BUILD_ROOT


%files server
%defattr(-,root,root,-)
%doc README COPYING
%{_datadir}/%{name}
%{_bindir}/start-bodhi
%config(noreplace) %{_sysconfdir}/%{name}.cfg

%files client
%doc COPYING README
%{_bindir}/bodhi


%changelog
* Sat Oct 16 2007 Luke Macken <lmacken@redhat.com> - 0.3.2-1
- 0.3.2
- Add COPYING file
- s/python-json/python-simplejson/

* Sat Oct  6 2007 Luke Macken <lmacken@redhat.com> - 0.3.1-1
- 0.3.1

* Wed Oct  3 2007 Luke Macken <lmacken@redhat.com> - 0.2.0-5
- Add python-fedora to bodhi-client Requires

* Mon Sep 17 2007 Luke Macken <lmacken@redhat.com> - 0.2.0-4
- Add python-json to bodhi-client Requires

* Sun Sep 16 2007 Luke Macken <lmacken@redhat.com> - 0.2.0-3
- Add cvs to bodhi-server Requires

* Thu Sep 15 2007 Luke Macken <lmacken@redhat.com> - 0.2.0-2
- Handle python-setuptools-devel changes in Fedora 8
- Update license to GPLv2+

* Thu Sep 13 2007 Luke Macken <lmacken@redhat.com> - 0.2.0-1
- Split spec file into client/server subpackages
