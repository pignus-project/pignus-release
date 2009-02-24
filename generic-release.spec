%define release_name Generic
%define dist_version 11

Summary:	Generic release files
Name:		generic-release
Version:	10.90
Release:	3
License:	GPLv2
Group:		System Environment/Base
Source:		%{name}-%{version}.tar.gz
Obsoletes:	redhat-release
Provides:	redhat-release = %{version}-%{release}
Provides:	system-release = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Conflicts:	fedora-release

%description
Generic release files such as yum configs and various /etc/ files that
define the release. This package explicitly is a replacement for the 
trademarked release package, if you are unable for any reason to abide by the 
trademark restrictions on that release package.

%package notes
Summary:	Release Notes
License:	Open Publication
Group:		System Environment/Base
Provides:	system-release-notes = %{version}-%{release}
Conflicts:	fedora-release-notes

%description notes
Generic release notes package. This package explicitly is a replacement 
for the trademarked release-notes package, if you are unable for any reason
to abide by the trademark restrictions on that release-notes 
package. Please note that there is no actual useful content here.


%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
echo "Generic release %{version} (%{release_name})" > $RPM_BUILD_ROOT/etc/fedora-release
echo "cpe://o:generic:generic:%{version}" > $RPM_BUILD_ROOT/etc/system-release-cpe
cp -p $RPM_BUILD_ROOT/etc/fedora-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/etc/issue
cp -p $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue
ln -s fedora-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s fedora-release $RPM_BUILD_ROOT/etc/system-release

install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg

install -m 644 RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Install all the keys, link the primary keys to primary arch files
# and to compat generic location
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
for arch in i386 x86_64 ppc ppc64
  do
  ln -s RPM-GPG-KEY-fedora-%{dist_version}-primary RPM-GPG-KEY-fedora-$arch
  ln -s RPM-GPG-KEY-fedora-test-%{dist_version}-primary RPM-GPG-KEY-fedora-test-$arch
done
ln -s RPM-GPG-KEY-fedora-%{dist_version}-primary RPM-GPG-KEY-fedora
ln -s RPM-GPG-KEY-fedora-test-%{dist_version}-primary RPM-GPG-KEY-fedora-test
popd

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in fedora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

install -d -m 755 $RPM_BUILD_ROOT/%{_datadir}/%{name}
for file in compose/*; do
  install -m 644 $file $RPM_BUILD_ROOT/%{_datadir}/%{name}
done

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT/etc/rpm
cat >> $RPM_BUILD_ROOT/etc/rpm/macros.dist << EOF
# dist macros.

%%fedora		%{dist_version}
%%dist		.fc%{dist_version}
%%fc%{dist_version}		1
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc GPL 
%config %attr(0644,root,root) /etc/fedora-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/*
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%config %attr(0644,root,root) /etc/rpm/macros.dist
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%files notes
%defattr(-,root,root,-)
%doc README.Generic-Release-Notes

%changelog
* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> 10.90-2
- drop Requires: system-release-notes

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 10.90-1
- 10.90

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 10-1
- Bump to 10, update repos

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 9.91-2
- add Conflicts
- further sanitize descriptions

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 9.91-1
- initial package for generic-release and generic-release-notes
