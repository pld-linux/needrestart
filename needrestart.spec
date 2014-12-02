%include	/usr/lib/rpm/macros.perl
Summary:	Check which daemons need to be restarted after library upgrades
Name:		needrestart
Version:	1.2
Release:	0.5
License:	GPL v2
Group:		Applications
Source0:	https://github.com/liske/needrestart/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9e5ecf1eab10a0a628641a6fed98608b
URL:		https://fiasko-nw.net/~thomas/tag/needrestart.html
BuildRequires:	rpm-perlprov >= 4.1-13
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
needrestart checks which daemons need to be restarted after library
upgrades. It is inspired by checkrestart from the debian-goodies
package.

Features:
- supports (but does not require) systemd
- binary blacklisting (i.e. display managers)
- tries to detect pending kernel upgrades
- tries to detect required restarts of interpreter based daemons
  (supports Perl, Python, Ruby)
- fully integrated into apt/dpkg using hooks

%prep
%setup -q

%build
cd perl
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/NeedRestart/.packlist
%{__rm} $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
%ifos Linux
%{__rm} $RPM_BUILD_ROOT%{perl_vendorlib}/NeedRestart/Kernel/kFreeBSD.pm
%endif
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/hook.d/10-dpkg
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/hook.d/30-pacman

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.* INSTALL NEWS README.Kernel
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/hook.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/needrestart.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/hook.d/20-rpm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/hook.d/90-none
%attr(755,root,root) %{_sbindir}/needrestart
%{perl_vendorlib}/NeedRestart.pm
%{perl_vendorlib}/NeedRestart
