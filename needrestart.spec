%include	/usr/lib/rpm/macros.perl
Summary:	Check which daemons need to be restarted after library upgrades
Name:		needrestart
Version:	2.0
Release:	0.10
License:	GPL v2
Group:		Applications
Source0:	https://github.com/liske/needrestart/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	21d04f18accdd1fc538b436e2c8dac0c
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
%setup -q -c
mv %{name}-*/* .

%{__rm} perl/lib/NeedRestart/UI/Debconf.pm

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
%doc AUTHORS ChangeLog README.* INSTALL NEWS
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/needrestart.conf
%dir %{_sysconfdir}/%{name}/hook.d
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/hook.d/20-rpm
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/hook.d/90-none
%dir %{_sysconfdir}/%{name}/conf.d
%attr(755,root,root) %{_sysconfdir}/%{name}/conf.d/README.needrestart
%dir %{_sysconfdir}/%{name}/notify.d
%{_sysconfdir}/%{name}/notify.d/README.needrestart
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/notify.d/200-write
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/notify.d/400-notify-send
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/notify.d/600-mail

%attr(755,root,root) %{_sbindir}/needrestart
%{_datadir}/polkit-1/actions/net.fiasko-nw.needrestart.policy

%{perl_vendorlib}/NeedRestart.pm
%{perl_vendorlib}/NeedRestart
