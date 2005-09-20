#
# Conditional build:
%bcond_with	gnome	# build gcdmaster
%bcond_without	mp3	# without MP3 support
%bcond_without	ogg	# without Ogg support
#
Summary:	Tools for burning CDRs in Disk At Once mode
Summary(pl):	Narzêdzia do wypalania p³yt w trybie Disk At Once
Summary(pt_BR):	Cdrdao - Escreve CD-Rs de áudio em modo "disk-at-once"
Name:		cdrdao
Version:	1.2.0
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://dl.sourceforge.net/cdrdao/%{name}-%{version}.tar.gz
# Source0-md5:	dc2bdef7a7c8973e678ba4a4a2d9cc7e
Source1:	%{name}.desktop
# http://cdrdao.sourceforge.net/drives.html#dt
Source2:	%{name}.drivers
Patch0:		%{name}-nolibs.patch
Patch1:		%{name}-pccts-antlr.patch
Patch2:		%{name}-gcc4.patch
URL:		http://cdrdao.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cdrtools-devel >= 3:2.01a25
%{?with_gnome:BuildRequires:	gtkmm-devel >= 2.4.0}
%{?with_mp3:BuildRequires:	lame-libs-devel >= 3.92}
%if %{with mp3} || %{with ogg}
BuildRequires:	libao-devel >= 0.8
%endif
%{?with_mp3:BuildRequires:	libmad-devel >= 0.15.1b-4}
%{?with_gnome:BuildRequires:	libgnomeuimm-devel >= 2.6.0}
BuildRequires:	libmad-devel >= 0.15.1b-4
%{?with_gnome:BuildRequires:	libsigc++-devel >= 2.0.0}
BuildRequires:	libstdc++-devel
%{?with_ogg:BuildRequires:	libvorbis-devel >= 1.0}
BuildRequires:	pccts >= 1.33MR33-8
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	%{name} = %{version}-%{release}

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
%patch2 -p1

sed -i -e 's#/usr/src/linux/include##g' scsilib/DEFAULT*/Defaults.linux
%if %{without gnome}
sed -i -e 's/^en_xdao=yes$/en_xdao=no/' configure.ac
%endif

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
PKG_CONFIG=%{_bindir}/pkg-config \
%configure \
	--with-pcctsbin=%{_bindir} \
	--with-pcctsinc=%{_libdir}/pccts/h \
	--with-scglib-inc=%{_includedir}/schily \
	--with-scglib-lib=%{_libdir} \
	--with%{!?with_gnome:out}-xdao \
	--with%{!?with_mp3:out}-mp3-support \
	--with%{!?with_ogg:out}-ogg-support

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_datadir}/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/gcdmaster.desktop
install xdao/stock/gcdmaster.png $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{name}/drivers

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS README README.PlexDAE 
%attr(755,root,root) %{_bindir}/cdrdao
%attr(755,root,root) %{_bindir}/toc2*
%attr(755,root,root) %{_bindir}/cue2toc
%{_datadir}/%{name}
%{_mandir}/man1/cdrdao.1*
%{_mandir}/man1/cue2toc.1*

%if %{with gnome}
%files gcdmaster
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gcdmaster
%{_desktopdir}/gcdmaster.desktop
%{_pixmapsdir}/*
%{_mandir}/man1/gcdmaster.*
%endif
