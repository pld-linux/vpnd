Summary:	Virtual Private Network Daemon
Summary(pl.UTF-8):	Daemon Wirtualnych Sieci Prywatnych (VPN)
Name:		vpnd
Version:	1.1.2
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://sunsite.dk/vpnd/archive/%{name}-%{version}.tar.gz
# Source0-md5:	6b8e18530b15801d2f0a2e443cc5c6ae
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://sunsite.dk/vpnd/
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
vpnd is a daemon which connects two networks on network level either
via TCP/IP or a (virtual) leased line attached to a serial interface.
All data transfered between the two networks are encrypted using the
unpatented free Blowfish encryption algorithm (see
http://www.counterpane.com/) with a key length of up to 576 bits (may
be downgraded to a minimum of 0 bits to suit any legal restrictions).

%description -l pl.UTF-8
vpnd jest demonem, który łączy dwie sieci poprzez TCP/IP lub
(wirtualną) linię dzierżawioną dołączoną do interfejsu szeregowego.
Wszystkie dane przesyłane pomiędzy sieciami są szyfrowane za pomocą
nieopatentowanego algorytmu Blowfish (zobacz
http://www.counterpane.com/) z kluczem długości do 576 bitów
(zmniejszanym do 0 by sprostać wszelkim prawnym restrykcjom).

%prep
%setup -q -n %{name}
find . -type f -print | xargs %{__sed} -i -e "s@/etc/vpnd\.@/etc/vpnd/vpnd.@g"
%{__sed} -i -e "s@-O3@%{rpmcflags} @g" -e "s@CC=gcc@CC=%{__cc}@" configure

%build
./configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/etc/sysconfig,/etc/rc.d/init.d}

install %{name}		$RPM_BUILD_ROOT%{_sbindir}
install %{name}.chat	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install %{name}.conf	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add vpnd
if [ -f %{_var}/lock/subsys/vpnd ]; then
	/etc/rc.d/init.d/vpnd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/vpnd start\" to start vtun daemons."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f %{_var}/lock/subsys/vpnd ]; then
		/etc/rc.d/init.d/vpnd stop >&2
	fi
	/sbin/chkconfig --del vpnd
fi

%files
%defattr(644,root,root,755)
%doc FAQ.TXT README SPEED.TXT VERSIONS samples
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(750,root,root) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%attr(755,root,root) %{_sbindir}/*
