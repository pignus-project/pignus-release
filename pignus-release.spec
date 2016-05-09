%global release_name Pignus
%global dist_version 26

Summary:        Pignus release files
Name:           pignus-release
Version:        26
Release:        0.1.pi1
License:        MIT
Group:	        System Environment/Base
Source0:        LICENSE
Source1:        README.developers
Source2:        README.Generic-Release-Notes
Source3:        README.license
Source4:        85-display-manager.preset
Source5:        90-default.preset
Source6:        99-default-disable.preset

# Pignus Koji configuration
Source665:      pignus-koji
Source666:      pignus-config
source667:      pignus-upload-ca.cert
Source668:      pignus-server-ca.cert

# Pigpkg configuration
Source669:      pigpkg
Source670:      pigpkg.conf

# Pignus mock configuration
Source671:      pignus-23-armv6hl.cfg
Source672:      pignus-24-armv6hl.cfg

# Pignus mash configuration
Source681:      pignus-23.base48.mash
Source682:      pignus-24.base48.mash
Source690:      mash.base48.conf

Obsoletes:      redhat-release
Provides:       redhat-release
Provides:       system-release
Provides:       system-release(%{version})
# Comment this next Requires out if we're building for a non-rawhide target
#Requires:       pignus-repos-rawhide
Requires:       pignus-repos(%{version})
Obsoletes:      pignus-release-rawhide <= 21-5
Obsoletes:      pignus-release-cloud <= 23-0.4
Obsoletes:      pignus-release-server <= 23-0.4
Obsoletes:      pignus-release-workstation <= 23-0.4
BuildArch:      noarch
Conflicts:      fedora-release
Conflicts:      generic-release

%description
Pignus release files such as yum configs and various /etc/ files that
define the release.

%package notes
Summary:	Release Notes
License:	Open Publication
Group:		System Environment/Base
Provides:	system-release-notes = %{version}-%{release}
Conflicts:	fedora-release-notes
Conflicts:	generic-release-notes

%description notes
Pignus release notes package.
Please note that there is no actual useful content here.

%package -n pignus-devel
Summary:	Pignus development files
License:	MIT
Group:		System Environment/Base
Requires:       mock koji fedpkg fedora-packager mash

%description -n pignus-devel
Configuration for Pignus development & release engineering.


%prep
%setup -c -T
cp -a %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} .

%build

%install
install -d %{buildroot}/etc
echo "Pignus %{version} (%{release_name})" > %{buildroot}/etc/system-release
echo "cpe:/o:pignus:pignus:%{version}" > %{buildroot}/etc/system-release-cpe
cp -p %{buildroot}/etc/system-release %{buildroot}/etc/issue
echo "Kernel \r on an \m (\l)" >> %{buildroot}/etc/issue
cp -p %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue
ln -s system-release %{buildroot}/etc/redhat-release
ln -s system-release %{buildroot}/etc/fedora-release

mkdir -p %{buildroot}/usr/lib/systemd/system-preset/

cat << EOF >>%{buildroot}/usr/lib/os-release
NAME=Pignus
VERSION="%{version} (%{release_name})"
ID=pignus
VERSION_ID=%{version}
PRETTY_NAME="Pignus %{version} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:pignus:pignus:%{version}"
EOF
# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}/etc/os-release

# Set up the dist tag macros
install -d -m 755 %{buildroot}%{_rpmconfigdir}/macros.d
cat >> %{buildroot}%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%fedora		%{dist_version}
%%dist		.fc%{dist_version}
%%fc%{dist_version}		1
EOF

# Add presets
# Default system wide
install -m 0644 85-display-manager.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 90-default.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 99-default-disable.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/

# Pignus development

# Pignus Koji configuration
install -d %{buildroot}%{_bindir}
install -m 0755 %{SOURCE665} %{buildroot}%{_bindir}/pignus-koji
install -d %{buildroot}%{_sysconfdir}/koji.conf.d
install -m 0644 %{SOURCE666} %{buildroot}%{_sysconfdir}/koji.conf.d/pignus-config
install -m 0644 %{SOURCE667} %{buildroot}%{_sysconfdir}/koji.conf.d/pignus-upload-ca.cert
install -m 0644 %{SOURCE668} %{buildroot}%{_sysconfdir}/koji.conf.d/pignus-server-ca.cert

# Pigpkg configuration
install -d %{buildroot}%{_bindir}
install -m 755 %{SOURCE669} %{buildroot}%{_bindir}/pigpkg
install -d %{buildroot}%{_sysconfdir}/rpkg
install -m 0644 %{SOURCE670} %{buildroot}%{_sysconfdir}/rpkg/pigpkg.conf

# Pignus mock configuration
install -d %{buildroot}%{_sysconfdir}/mock
install -m 0644 %{SOURCE671} %{SOURCE672} %{buildroot}%{_sysconfdir}/mock/

# Pignus mash configuration
install -d %{buildroot}%{_sysconfdir}/mash
install -m 0644 %{SOURCE681} %{SOURCE682} %{buildroot}%{_sysconfdir}/mash/
install -m 0644 %{SOURCE690} %{buildroot}%{_sysconfdir}/mash/mash.base48.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%license LICENSE README.license
%config %attr(0644,root,root) /usr/lib/os-release
/etc/os-release
%config %attr(0644,root,root) /etc/system-release
/etc/redhat-release
/etc/fedora-release
%config %attr(0644,root,root) /etc/system-release-cpe
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset

%files notes
%defattr(-,root,root,-)
%doc README.Generic-Release-Notes

%files -n pignus-devel
%dir %{_sysconfdir}/koji.conf.d
%{_sysconfdir}/koji.conf.d/pignus-config
%{_sysconfdir}/koji.conf.d/pignus-server-ca.cert
%{_sysconfdir}/koji.conf.d/pignus-upload-ca.cert
%dir %{_sysconfdir}/rpkg
%{_sysconfdir}/rpkg/pigpkg.conf
%{_bindir}/pignus-koji
%{_bindir}/pigpkg
%dir %{_sysconfdir}/mock
%{_sysconfdir}/mock/pignus-*-armv6hl.cfg
%dir %{_sysconfdir}/mash
%{_sysconfdir}/mash/pignus-*.base48.mash
%{_sysconfdir}/mash/mash.base48.conf

%changelog
* Sat Apr 08 2017 Lubomir Rintel <lkudrak@v3.sk> - 26-0.1.pi1
- Turn generic-release into pignus-release
- Add a pignus-devel subpackage

* Thu Aug 04 2016 Bruno Wolff III <bruno@wolff.to> - 26-0.1
- Rawhide is now 26

* Sat Mar 05 2016 Bruno Wolff III <bruno@wolff.to> - 25-0.1
- Rawhide is now 25

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 24-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Tom Callaway <spot@fedoraproject.org> - 24-0.3
- spec file cleanups

* Sat Aug 22 2015 Bruno Wolff III <bruno@wolff.to> - 24-0.2
- Fix typo in obsoletes

* Wed Jul 15 2015 Bruno Wolff III <bruno@wolff.to> - 24-0.1
- Rawhide is now f24

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 23-0.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Dennis Gilmore <dennis@ausil.us> - 23-0.5
- add system preset files
- drop product sub-packages

* Sat Feb 14 2015 Bruno Wolff III <bruno@wolff.to> - 23-0.4
- Fix up change log

* Sat Feb 14 2015 Bruno Wolff III <bruno@wolff.to> - 23-0.3
- Rawhide is now 23

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
