Summary:	Small queueing SMTP relayer
Summary(pl):	Ma³y agent SMTP relay kolejkuj±cy pocztê
Name:		omta
Version:	0.51
Release:	1
Vendor:		Wouter Coene <wottie@dds.nl>
URL:		http://huizen.dds.nl/~wottie/omta/
Source0:	%{name}-%{version}.tar.gz
Patch0:		%{name}-FHS.patch
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
License:	GPL
Provides:	smtpdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OMTA is an SMTP server tool wich allows people who have a dialup connection
to queue their mail on their hard disk, and send it to their SMTP server
whenever they are online.

OMTA has the following features:
- Works transparently by simulating SENDMAIL.
- Can relay messages to another SMTP server.
- It can also deliver local mail (trough procmail or similar).
- Has built-in SMTP server for the local machine.
- Users can (safely!) set their own private configuration, including From
  address.
- Built around the K.I.S.S. principle ("Keep It Simple, Stupid!")

%description -l pl
OMTA jest narzêdziem SMTP który umo¿liwia ludziom bez sta³ego dostêpu do
sieci kolejkowaæ pocztê na dysku, i wysy³aæ j± do swojego serwera SMTP
kiedy tylko s± online.

OMTA ma nastêpuj±ce cechy:
- Pracuje "przezroczy¶cie", udaj±c SENDMAILa
- Mo¿e przesy³aæ listy do innego serwera SMTP
- Mo¿e te¿ dostarczaæ lokalnie pocztê (przez procmaila lub podobne)
- Ma wbudowany serwer SMTP dla lokalnej maszyny
- U¿ytkonicy mog± (bezpiecznie!) ustawiaæ ich w³asn± konfiguracjê,
  w³±czaj±c w to adresy From
- Zbudowany w oparciu o zasadê K.I.S.S ("Keep It Simple, Stupid!")

%prep
%setup -q
%patch0 -p1

%build
LDFLAGS="-s"; export LDFLAGS
aclocal
autoconf
automake
autoheader
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
install -d $RPM_BUILD_ROOT/var/omta/queue
install -d $RPM_BUILD_ROOT%{_libdir}
ln -sf %{_bindir}/omta $RPM_BUILD_ROOT%{_libdir}/sendmail
ln -sf %{_bindir}/omta $RPM_BUILD_ROOT%{_bindir}/sendmail
mv omta.conf.dist omta.conf
gzip -9nf FAQ README AUTHORS CHANGES omta.conf \
	$RPM_BUILD_ROOT/%{_mandir}/man*/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%dir %attr(770,root,mail) /var/omta/queue
%attr(2755,root,mail) %{_bindir}/omta
%{_mandir}/man*/*
%{_bindir}/mailq
%{_bindir}/sendmail
%{_libdir}/sendmail
