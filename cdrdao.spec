#
# Conditional build:
%bcond_without	gnome	# don't build gcdmaster
%bcond_without	mp3	# without MP3 support
%bcond_without	ogg	# without Ogg support
#
Summary:	Tools for burning CDRs in Disk At Once mode
Summary(pl.UTF-8):	Narzędzia do wypalania płyt w trybie Disk At Once
Summary(pt_BR.UTF-8):	Cdrdao - Escreve CD-Rs de áudio em modo "disk-at-once"
Name:		cdrdao
Version:	1.2.6
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	https://downloads.sourceforge.net/cdrdao/%{name}-%{version}.tar.bz2
# Source0-md5:	f59689d847d56647187d4de487e3487d
Source1:	%{name}.desktop
# http://cdrdao.sourceforge.net/drives.html#dt
Source2:	%{name}.drivers
Patch0:		%{name}-nolibs.patch
Patch1:		%{name}-pccts-antlr.patch
Patch2:		%{name}-gcc4.patch
URL:		http://cdrdao.sourceforge.net/
%{?with_gnome:BuildRequires:	gtkmm3-devel >= 3.0.0}
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_gnome:BuildRequires:	libsigc++-devel >= 2.0.0}
BuildRequires:	lame-libs-devel
%{?with_mp3:BuildRequires:	lame-libs-devel}
%if %{with mp3} || %{with ogg}
BuildRequires:	libao-devel >= 0.8
%endif
BuildRequires:	libmad-devel >= 0.15.1b-4
%{?with_mp3:BuildRequires:	libmad-devel >= 0.15.1b-4}
BuildRequires:	libstdc++-devel
%{?with_ogg:BuildRequires:	libvorbis-devel >= 1:1.0}
BuildRequires:	pccts >= 1.33MR33-8
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cdrdao records audio and data CD-Rs in Disk At Once mode. This mode
gives much better control over contents of CD.

%description -l pl.UTF-8
Cdrdao zapisuje płytki audio i z danymi w trybie Disk At Once. W tym
trybie masz znacznie większą kontrolę nad zawartością płytki.

%description -l pt_BR.UTF-8
Escreve CD-Rs de áudio em modo "disk-at-once" (DAO) permitindo
controle sobre pre-gaps (tamanho reduzido a 0, dados não zerados de
áudio) e informações de sub-canais como códigos ISRC. Todos os dados
que são escritos no disco devem ser especificados através de um
arquivo texto. Dados de áudio também podem estar no formato WAVE ou
raw.

%package gcdmaster
Summary:	GTK+ 3 frontend to cdrdao for composing audio CDs
Summary(pl.UTF-8):	Frontend GTK+ 3 do cdrdao do składania płyt CD-Audio
Group:		X11/Applications
Requires(post,postun):	shared-mime-info
Requires:	%{name} = %{version}-%{release}

%description gcdmaster
gcdmaster allows the creation of toc-files for cdrdao and can control
the recording process. Its main application is the composition of
audio CDs from one or more audio files. It supports PQ-channel
editing, entry of meta data like ISRC codes/CD-TEXT and non
destructive cut of the audio data.

%description gcdmaster -l pl.UTF-8
gcdmaster pozwala na tworzenie plików toc dla cdrdao oraz może
kontrolować proces nagrywania. Głównym celem jest składanie płyt
CD-Audio z jednego lub więcej plików z dźwiękiem. Obsługuje edycję
kanału PQ, wpisy meta-danych takich jak kody ISRC/CD-TEXT oraz
niedestruktywne cięcie danych audio.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
#%patch -P2 -p1

%if %{without gnome}
%{__sed} -i \
	-e 's/^en_gcdmaster=yes$/en_gcdmaster=no/' \
	configure.ac
%endif

# we use our own .desktop file with more translations
cp -p %{SOURCE1} gcdmaster/gcdmaster.desktop

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
PKG_CONFIG=%{_bindir}/pkg-config \
%configure \
	--with-pcctsbin=%{_bindir} \
	--with-pcctsinc=%{_includedir}/pccts/h \
	--with%{!?with_gnome:out}-gcdmaster \
	--with%{!?with_mp3:out}-mp3-support \
	--with%{!?with_ogg:out}-ogg-support

%{__make} \
	CC="%{__cc}" \
	COPTOPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{name}/drivers

# legacy GNOME stuff
rm -rf $RPM_BUILD_ROOT%{_datadir}/{application-registry,mime-info}

%clean
rm -rf $RPM_BUILD_ROOT

%post gcdmaster
%update_mime_database
%glib_compile_schemas

%postun gcdmaster
%update_mime_database
%glib_compile_schemas

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS README README.PlexDAE README.Win32
%attr(755,root,root) %{_bindir}/cdrdao
%attr(755,root,root) %{_bindir}/toc2*
%attr(755,root,root) %{_bindir}/cue2toc
%{_datadir}/%{name}
%{_mandir}/man1/cdrdao.1*
%{_mandir}/man1/cue2toc.1*
%{_mandir}/man1/toc2cddb.1*
%{_mandir}/man1/toc2cue.1*

%if %{with gnome}
%files gcdmaster
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gcdmaster
%{_datadir}/gcdmaster
%{_datadir}/mime/packages/gcdmaster.xml
%{_desktopdir}/gcdmaster.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.gcdmaster.gschema.xml
%{_pixmapsdir}/*
%{_mandir}/man1/gcdmaster.1*
%endif
