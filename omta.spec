Summary:	Small queueing SMTP relayer
Summary(pl):	Ma³y agent SMTP relay kolejkuj±cy pocztê
Name:		omta
Version:	0.51
Release:	9
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://omta.runlevel.net/pub/omta/%{name}-%{version}.tar.gz
Patch0:		%{name}-FHS.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-omta.conf_path.patch
URL:		http://omta.runlevel.net
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
Provides:	smtpdaemon
Obsoletes:	smtpdaemon
Obsoletes:	exim
Obsoletes:	masqmail
Obsoletes:	postfix
Obsoletes:	qmail
Obsoletes:	sendmail
Obsoletes:	sendmail-cf
Obsoletes:	sendmail-doc
Obsoletes:	smail
Obsoletes:	zmailer
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_spooldir	/var/spool/omtaqueue
%define		_sysconfdir	/etc/mail

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

%prep -q
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
rm -f missing
gettextize --copy --force
aclocal
autoheader
%{__autoconf}
%{__automake}
(cd libgetconf
rm -f missing
aclocal
%{__autoconf}
automake -a -c)
%configure \
	--with-queuepath=%{_spooldir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_spooldir},%{_libdir},%{_sbindir},%{_sysconfdir}}

%{__make} DESTDIR=$RPM_BUILD_ROOT install

ln -sf %{_bindir}/omta $RPM_BUILD_ROOT%{_libdir}/sendmail
ln -sf %{_bindir}/omta $RPM_BUILD_ROOT%{_sbindir}/sendmail
mv -f omta.conf.dist $RPM_BUILD_ROOT%{_sysconfdir}/omta.conf

gzip -9nf FAQ README AUTHORS CHANGES

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(2755,root,mail) %{_bindir}/omta
%attr(755,root,root) %{_bindir}/mailq
%attr(755,root,root) %{_libdir}/sendmail
%attr(755,root,root) %{_sbindir}/sendmail
%dir %{_sysconfdir}
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/omta.conf
%dir %attr(770,root,mail) %{_spooldir}
%{_mandir}/man*/*
