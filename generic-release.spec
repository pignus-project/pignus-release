%define release_name Generic
%define dist_version 15

Summary:	Generic release files
Name:		generic-release
Version:	15
Release:	0.3
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

%package rawhide
Summary:        Rawhide repo definitions
Requires:	generic-release = %{version}-%{release}
Conflicts:	fedora-release-rawhide

%description rawhide
This package provides the rawhide repo definitions.

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
for arch in i386 x86_64
  do
  ln -s RPM-GPG-KEY-fedora-%{dist_version}-primary RPM-GPG-KEY-fedora-$arch
done
ln -s RPM-GPG-KEY-fedora-%{dist_version}-primary RPM-GPG-KEY-fedora
for arch in sparc sparc64
  do
  ln -s RPM-GPG-KEY-fedora-%{dist_version}-SPARC RPM-GPG-KEY-fedora-$arch
done
popd

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in fedora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
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
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates*.repo
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%config %attr(0644,root,root) /etc/rpm/macros.dist
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%files notes
%defattr(-,root,root,-)
%doc README.Generic-Release-Notes

%files rawhide
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo

%changelog
* Wed Oct 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 15-0.3
- sync to rawhide

* Wed Feb 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 14-0.2
- fix broken requires

* Wed Feb 17 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 14-0.1
- update to sync with fedora-release

* Mon Nov 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 12-1
- Update for F12 final

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 11.90-1
- Build for F12 collection

* Wed May 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 11-1
- resync with fedora-release package

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
