Summary:	Small queueing SMTP relayer
Summary(pl):	Ma³y agent SMTP relay kolejkuj±cy pocztê
Name:		omta
Version:	0.51
Release:	14
License:	GPL
Group:		Networking/Daemons
#Source0:	ftp://omta.runlevel.net/pub/omta/%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	5a07f592292dce29b584d9745beb30ce
Source1:	%{name}.inetd
Patch0:		%{name}-FHS.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-%{name}.conf_path.patch
Patch3:		%{name}-configure.patch
# Homepage/domain no longer exists
#URL:		http://omta.runlevel.net/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
Provides:	smtpdaemon
Obsoletes:	courier
Obsoletes:	exim
Obsoletes:	masqmail
Obsoletes:	nullmailer
Obsoletes:	postfix
Obsoletes:	qmail
Obsoletes:	sendmail
Obsoletes:	sendmail-cf
Obsoletes:	sendmail-doc
Obsoletes:	smail
Obsoletes:	smtpdaemon
Obsoletes:	sstmp
Obsoletes:	zmailer
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_spooldir	/var/spool/omtaqueue

%description
OMTA is an SMTP server tool wich allows people who have a dialup
connection to queue their mail on their hard disk, and send it to
their SMTP server whenever they are online.

OMTA has the following features:
- Works transparently by simulating SENDMAIL.
- Can relay messages to another SMTP server.
- It can also deliver local mail (trough procmail or similar).
- Has built-in SMTP server for the local machine.
- Users can (safely!) set their own private configuration, including
  From address.
- Built around the K.I.S.S. principle ("Keep It Simple, Stupid!")

%description -l pl
OMTA jest narzêdziem SMTP który umo¿liwia ludziom bez sta³ego dostêpu
do sieci kolejkowaæ pocztê na dysku i wysy³aæ j± do swojego serwera
SMTP kiedy tylko s± online.

OMTA ma nastêpuj±ce cechy:
- Pracuje "przezroczy¶cie", udaj±c SENDMAILa
- Mo¿e przesy³aæ listy do innego serwera SMTP
- Mo¿e te¿ dostarczaæ lokalnie pocztê (przez procmaila lub podobne)
- Ma wbudowany serwer SMTP dla lokalnej maszyny
- U¿ytkownicy mog± (bezpiecznie!) ustawiaæ ich w³asn± konfiguracjê,
  w³±czaj±c w to adresy From
- Zbudowany w oparciu o zasadê K.I.S.S ("Keep It Simple, Stupid!")

%package smtp
Summary:	Omta SMTP local server
Summary(pl):	Lokalny serwer SMTP omta
Group:		Networking/Daemons
Requires:	%{name} = %{version}
Requires:	rc-inetd

%description smtp
Setup tcp/25 on localhost with omta-smtp.

%description smtp -l pl
Pakiet w³±czaj±cy omta-smtp na porcie tcp/25 dla tej maszyny.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
cd libgetconf
%{__aclocal}
%{__autoconf}
%{__automake}
cd ..
%configure \
	--with-queuepath=%{_spooldir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_spooldir},%{_prefix}/lib,%{_sbindir},%{_sysconfdir}/{mail,sysconfig/rc-inetd}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf %{_bindir}/omta $RPM_BUILD_ROOT%{_prefix}/lib/sendmail
ln -sf %{_bindir}/omta $RPM_BUILD_ROOT%{_sbindir}/sendmail
ln -sf %{_bindir}/omta $RPM_BUILD_ROOT%{_sbindir}/in.smtpd
mv -f omta.conf.dist $RPM_BUILD_ROOT%{_sysconfdir}/mail/omta.conf

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/smtpd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc FAQ README AUTHORS CHANGES
%dir %attr(770,root,mail) %{_spooldir}
%dir %{_sysconfdir}/mail
%attr(2755,root,mail) %{_bindir}/omta
%attr(755,root,root) %{_bindir}/mailq
%attr(755,root,root) %{_prefix}/lib/sendmail
%attr(755,root,root) %{_sbindir}/sendmail
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/mail/omta.conf
%{_mandir}/man*/*

%files smtp
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/in.smtpd
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/smtpd
