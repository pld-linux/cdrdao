#
# Conditional build:
# _without_gnome	- without GNOME frontend (gcdmaster)
#
Summary:	Tools for burning CDRs in Disk At Once mode
Summary(pl):	Narz�dzia do wypalania p�yt w trybie Disk At Once
Summary(pt_BR):	Cdrdao - Escreve CD-Rs de �udio em modo "disk-at-once"
Name:		cdrdao
Version:	1.1.5
Release:	2
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/cdrdao/%{name}-%{version}.src.tar.gz
Patch0:		%{name}-destdir.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-acfix.patch
Patch3:		%{name}-gcdmaster-paths.patch
URL:		http://cdrdao.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	libstdc++-devel
BuildRequires:	libsigc++-devel
BuildRequires:	pccts-devel
%{!?_without_gnome:BuildRequires:	gtkmm-devel >= 1.2.5}
%{!?_without_gnome:BuildRequires:	gnome-libs-devel >= 1.2.3}
%{!?_without_gnome:BuildRequires:	gnomemm-devel >= 1.1.17}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_xprefix	/usr/X11R6
%define		_xbindir	%{_xprefix}/bin
%define		_xmandir	%{_xprefix}/man

%description
Cdrdao records audio and data CD-Rs in Disk At Once mode. This mode
gives much better control over contents of CD.

%description -l pl
Cdrdao zapisuje p�ytki audio i z danymi w trybie Disk At Once. W tym
trybie masz znacznie wi�ksz� kontrol� nad zawarto�ci� p�ytki.

%description -l pt_BR
Escreve CD-Rs de �udio em modo "disk-at-once" (DAO) permitindo
controle sobre pre-gaps (tamanho reduzido a 0, dados n�o zerados de
�udio) e informa��es de sub-canais como c�digos ISRC. Todos os dados
que s�o escritos no disco devem ser especificados atrav�s de um
arquivo texto. Dados de �udio tamb�m podem estar no formato WAVE ou
raw.

%package gcdmaster
Summary:	GNOME frontend to cdrdao for composing audio CDs
Summary(pl):	Frontend GNOME do cdrdao do sk�adania p�yt CD-Audio
Group:		X11/Applications
Group(de):	X11/Applikationen
Group(es):	X11/Aplicaciones
Group(pl):	X11/Aplikacje
Group(pt_BR):	X11/Aplica��es
Group(pt):	X11/Aplica��es
Requires:	%{name} = %{version}

%description gcdmaster
gcdmaster allows the creation of toc-files for cdrdao and can control
the recording process. Its main application is the composition of
audio CDs from one or more audio files. It supports PQ-channel
editing, entry of meta data like ISRC codes/CD-TEXT and non
destructive cut of the audio data.

%description gcdmaster -l pl
gcdmaster pozwala na tworzenie plik�w toc dla cdrdao oraz mo�e
kontrolowa� proces nagrywania. G��wnym celem jest sk�adanie p�yt
CD-Audio z jednego lub wi�cej plik�w z d�wi�kiem. Obs�uguje edycj�
kana�u PQ, wpisy meta-danych takich jak kody ISRC/CD-TEXT oraz
niedestruktywne ci�cie danych audio.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
(cd paranoia ; autoconf)
autoconf
# false gtkmm-config path can be used to disable building of GNOME frontend
%configure \
	--with-pcctsbin=%{_bindir} \
	--with-pcctsinc=%{_includedir}/pccts \
	%{?_without_gnome:--with-gtkmm-exec-prefix=/}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

gzip -9nf CREDITS README README.PlexDAE Release*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_mandir}/*/*

%if %{?_without_gnome:0}%{!?_without_gnome:1}
%files gcdmaster
%defattr(644,root,root,755)
%attr(755,root,root) %{_xbindir}/*
%{_xmandir}/man1/*
%{_pixmapsdir}/*
%{_applnkdir}/Applications/gcdmaster.desktop
%endif
