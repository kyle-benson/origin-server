Name:           stickshift-selinux
Version:        1.0.3
Release:        1%{?dist}
Summary:        Stickshift SELinux policies

License:        GPLv2
URL:            http://openshift.redhat.com
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       selinux-policy selinux-policy-targeted
Requires:       policycoreutils-python

%description
Stickshfit SELinux policies from the master_contrib and master
branches of selinux-policy at commit c2f865d.

git://git.fedorahosted.org/selinux-policy.git

%prep
%setup -q


%build
for sfx in fc if te
do
    if [ -f "openshift-backport%{dist}.${sfx}.disabled" ]
    then
        ln -sf "openshift-backport%{dist}.${sfx}.disabled" "openshift-backport.${sfx}"
    fi
done

make -f /usr/share/selinux/devel/Makefile
bzip2 *.pp

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_datadir}/selinux/packages/%{name}
mkdir -p %{buildroot}%{_datadir}/selinux/devel/include/services

install -m 644 *.pp.bz2        %{buildroot}%{_datadir}/selinux/packages/%{name}
install -m 644 *.if            %{buildroot}%{_datadir}/selinux/devel/include/services

%post
semodule -i %{_datadir}/selinux/packages/%{name}/*.pp.bz2

%preun
if [ $1 = 0 ]
then
    pkgs=()
    for pkg in %{_datadir}/selinux/packages/%{name}/*.pp.bz2
    do
        pkgs=("${pkgs[@]}" `basename "$pkg" .pp.bz2`)
    done
    semodule -r "${pkgs[@]}"
fi

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_datadir}/selinux/packages/%{name}/
%{_datadir}/selinux/devel/include/services/*.if

%changelog
* Fri Oct 05 2012 Rob Millner <rmillner@redhat.com> 1.0.3-1
- The dist macro uses fc rather than just f. (rmillner@redhat.com)
- Use openshift-backport policy instead (rmillner@redhat.com)
- Add Fedora 17 and 16 policy support and mechanism to select them on build.
  (rmillner@redhat.com)
- Update description (rmillner@redhat.com)
- Back-ported build requirements from Fedora 17 (rmillner@redhat.com)
- Add preun and dont touch autorelabel. (rmillner@redhat.com)

* Fri Oct 05 2012 Rob Millner <rmillner@redhat.com> 1.0.2-1
- Create new openshift-support module to carry Openshift related policies from
  other modules. (rmillner@redhat.com)
- Update SELinux policies to commit c2f865d (rmillner@redhat.com)
- Fix license for selinux (rmillner@redhat.com)
- Force relabel on next reboot after pkg install. (rmillner@redhat.com)
- Clean up selinux specfile (rmillner@redhat.com)
- Automatic commit of package [stickshift-selinux] release [1.0.1-1].
  (rmillner@redhat.com)
- Switch to openshift policies. (rmillner@redhat.com)
- Move policy build to the build phase and do installation in %%post
  (rmillner@redhat.com)


* Mon Oct 01 2012 Rob Millner <rmillner@redhat.com> 1.0.1-1
- Updated to openshift 1.0 policies


* Fri Sep 28 2012 Rob Millner <rmillner@redhat.com> 0.1.1-1
- Move stickshift selinux policies into their own RPM.

