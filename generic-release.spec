%define release_name Generic
%define dist_version 21

Summary:	Generic release files
Name:		generic-release
Version:	22
Release:	0.3
License:	MIT
Group:		System Environment/Base
Source0:	LICENSE
Source1:	README.developers
Source2:	README.Generic-Release-Notes
Source3:	80-server.preset
Source4:	README.license
Obsoletes:	redhat-release
Provides:	redhat-release
Provides:	system-release
Provides:	system-release(%{version})
Requires:       system-release-product
# Comment this next Requires out if we're building for a non-rawhide target
Requires:	fedora-repos-rawhide
Requires:	fedora-repos(%{version})
Obsoletes:	generic-release-rawhide <= 21-5
BuildArch:	noarch
Conflicts:	fedora-release

%description
Generic release files such as yum configs and various /etc/ files that
define the release. This package explicitly is a replacement for the 
trademarked release package, if you are unable for any reason to abide by the 
trademark restrictions on that release package.

%package nonproduct
Summary:        Base package for non-product-specific default configurations
Provides:       system-release-nonproduct
Provides:       system-release-nonproduct(%{version})
Provides:       system-release-product
# turned out to be a bad name
Requires:       generic-release = %{version}-%{release}
Conflicts:      generic-release-cloud
Conflicts:      generic-release-server
Conflicts:      generic-release-workstation

%description nonproduct
ITS NOT A PRODUCT. Er, em, what I meant to say was: This package 
provides a base package for non-product-specific configuration files to
depend on.

%package cloud
Summary:        Base package for Generic Cloud-specific default configurations
Provides:       system-release-cloud
Provides:       system-release-cloud(%{version})
Provides:       system-release-product
Requires:       generic-release = %{version}-%{release}
Conflicts:      generic-release-server
Conflicts:      generic-release-nonproduct
Conflicts:      generic-release-workstation

%description cloud
Provides a base package for Generic Cloud-specific configuration files to
depend on.

%package server
Summary:        Base package for Generic Server-specific default configurations
Provides:       system-release-server
Provides:       system-release-server(%{version})
Provides:       system-release-product
Requires:       generic-release = %{version}-%{release}
#Inheriting Fedora's Requires. You don't like em? Make your own -release-server package.
Requires:       systemd
Requires:       cockpit
Requires:       rolekit
Requires(post): sed
Requires(post): systemd
Conflicts:      generic-release-cloud
Conflicts:      generic-release-nonproduct
Conflicts:      generic-release-workstation

%description server
Provides a base package for Generic Server-specific configuration files to
depend on.

%package workstation
Summary:        Base package for Generic Workstation-specific default configurations
Provides:       system-release-workstation
Provides:       system-release-workstation(%{version})
Provides:       system-release-product
Requires:       generic-release = %{version}-%{release}
Conflicts:      generic-release-cloud
Conflicts:      generic-release-server
Conflicts:      generic-release-nonproduct

%description workstation
Provides a base package for Generic Workstation-specific configuration files to
depend on.

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
%setup -c -T
cp -a %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE4} .

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
echo "Generic release %{version} (%{release_name})" > $RPM_BUILD_ROOT/etc/fedora-release
echo "cpe:/o:generic:generic:%{version}" > $RPM_BUILD_ROOT/etc/system-release-cpe
cp -p $RPM_BUILD_ROOT/etc/fedora-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/etc/issue
cp -p $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue
ln -s fedora-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s fedora-release $RPM_BUILD_ROOT/etc/system-release

cat << EOF >>$RPM_BUILD_ROOT/etc/os-release
NAME=Generic
VERSION="%{version} (%{release_name})"
ID=generic
VERSION_ID=%{version}
PRETTY_NAME="Generic %{version} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:generic:generic:%{version}"
EOF

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat >> $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%fedora		%{dist_version}
%%dist		.fc%{dist_version}
%%fc%{dist_version}		1
EOF

# Add Product-specific presets
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
# Fedora Server
install -m 0644 %{SOURCE3} %{buildroot}%{_prefix}/lib/systemd/system-preset/80-server.preset

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE README.license
%config %attr(0644,root,root) /etc/os-release
%config %attr(0644,root,root) /etc/fedora-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist

%files notes
%defattr(-,root,root,-)
%doc README.Generic-Release-Notes

%files nonproduct
%{!?_licensedir:%global license %%doc}
%license LICENSE

%files cloud
%{!?_licensedir:%global license %%doc}
%license LICENSE

%files server
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_prefix}/lib/systemd/system-preset/80-server.preset

%files workstation
%{!?_licensedir:%global license %%doc}
%license LICENSE

%changelog
* Tue Oct 21 2014 Tom Callaway <spot@fedoraproject.org> - 22-0.3
- add versioned provide for system-release(VERSION)

* Tue Oct 21 2014 Tom Callaway <spot@fedoraproject.org> - 22-0.2
- add productization (it is the foooooture)

* Thu Aug 07 2014 Dennis Gilmore <dennis@ausil.us> - 22-0.1
- Require fedora-repos and no longer ship repo files

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Tom Callaway <spot@fedoraproject.org> - 21-4
- license changes and clarification doc

* Sun Mar 09 2014 Bruno Wolff III <bruno@wolff.to> - 21-3
- Install dist macro into the correct directory

* Sun Jan 05 2014 Bruno Wolff III <bruno@wolff.to> - 21-2
- Work around incorrect prefix in the upstream tarball

* Sun Jan 05 2014 Bruno Wolff III <bruno@wolff.to> - 21-1
- Bump version to match current rawhide

* Sat Dec 21 2013 Bruno Wolff III <bruno@wolff.to> - 21-0.3
- Update version to 21 (which should have happened when f20 was branched)
- Changed to work with recent yum change (bug 1040607)

* Mon Dec  9 2013 Tom Callaway <spot@fedoraproject.org> - 20-1
- final release (disable rawhide dep)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 26 2013 Tom Callaway <spot@fedoraproject.org> - 20-0.1
- sync

* Wed Jun 26 2013 Tom Callaway <spot@fedoraproject.org> - 19-2
- sync to release

* Mon Mar 11 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 19-0.3
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 19-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Tom Callaway <spot@fedoraproject.org> - 19-0.1
- sync to 19-0.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 18-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Tom Callaway <spot@fedoraproject.org> - 18-0.2
- sync with fedora-release model

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Tom Callaway <spot@fedoraproject.org> - 17-0.2
- initial 17

* Fri Jul 22 2011 Tom Callaway <spot@fedoraproject.org> - 16-0.2
- require -rawhide subpackage if we're built for rawhide

* Fri May 13 2011 Tom Callaway <spot@fedoraproject.org> - 16-0.1
- initial 16

* Fri May 13 2011 Tom Callaway <spot@fedoraproject.org> - 15-1
- sync to f15 final

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

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
