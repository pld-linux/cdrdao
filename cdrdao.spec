#
# Conditional build:
# _without_gnome	- without GNOME frontend (gcdmaster)
#
Summary:	Tools for burning CDRs in Disk At Once mode
Summary(pl):	Narzêdzia do wypalania p³yt w trybie Disk At Once
Summary(pt_BR):	Cdrdao - Escreve CD-Rs de áudio em modo "disk-at-once"
Name:		cdrdao
Version:	1.1.7
Release:	2
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/cdrdao/%{name}-%{version}.src.tar.bz2
Patch0:		%{name}-destdir.patch
Patch1:		%{name}-opt.patch
Patch3:		%{name}-gcdmaster-paths.patch
URL:		http://cdrdao.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
%{!?_without_gnome:BuildRequires:	gnome-libs-devel >= 1.2.3}
%{!?_without_gnome:BuildRequires:	gnomemm-devel >= 1.1.17}
%{!?_without_gnome:BuildRequires:	gtkmm-devel >= 1.2.5}
BuildRequires:	libstdc++-devel
BuildRequires:	libsigc++1-devel
BuildRequires:	pccts >= 1.33MR33-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_xprefix	/usr/X11R6
%define		_xbindir	%{_xprefix}/bin
%define		_xmandir	%{_xprefix}/man

%description
Cdrdao records audio and data CD-Rs in Disk At Once mode. This mode
gives much better control over contents of CD.

%description -l pl
Cdrdao zapisuje p³ytki audio i z danymi w trybie Disk At Once. W tym
trybie masz znacznie wiêksz± kontrolê nad zawarto¶ci± p³ytki.

%description -l pt_BR
Escreve CD-Rs de áudio em modo "disk-at-once" (DAO) permitindo
controle sobre pre-gaps (tamanho reduzido a 0, dados não zerados de
áudio) e informações de sub-canais como códigos ISRC. Todos os dados
que são escritos no disco devem ser especificados através de um
arquivo texto. Dados de áudio também podem estar no formato WAVE ou
raw.

%package gcdmaster
Summary:	GNOME frontend to cdrdao for composing audio CDs
Summary(pl):	Frontend GNOME do cdrdao do sk³adania p³yt CD-Audio
Group:		X11/Applications
Requires:	%{name} = %{version}

%description gcdmaster
gcdmaster allows the creation of toc-files for cdrdao and can control
the recording process. Its main application is the composition of
audio CDs from one or more audio files. It supports PQ-channel
editing, entry of meta data like ISRC codes/CD-TEXT and non
destructive cut of the audio data.

%description gcdmaster -l pl
gcdmaster pozwala na tworzenie plików toc dla cdrdao oraz mo¿e
kontrolowaæ proces nagrywania. G³ównym celem jest sk³adanie p³yt
CD-Audio z jednego lub wiêcej plików z d¼wiêkiem. Obs³uguje edycjê
kana³u PQ, wpisy meta-danych takich jak kody ISRC/CD-TEXT oraz
niedestruktywne ciêcie danych audio.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch3 -p1

%build
cd paranoia
%{__autoconf}
cd ..
cp -f /usr/share/automake/config.* .
%{__autoconf}
# false gtkmm-config path can be used to disable building of GNOME frontend
%configure \
	--with-pcctsbin=%{_bindir} \
	--with-pcctsinc=/usr/lib/pccts/h \
	%{?_without_gnome:--with-gtkmm-exec-prefix=/}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS README README.PlexDAE Release*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/cdrdao
%{_mandir}/*/*

%if %{?_without_gnome:0}%{!?_without_gnome:1}
%files gcdmaster
%defattr(644,root,root,755)
%attr(755,root,root) %{_xbindir}/*
%{_xmandir}/man1/*
%{_pixmapsdir}/*
%{_applnkdir}/Applications/gcdmaster.desktop
%endif
