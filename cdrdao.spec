#
# Conditional build:
%bcond_with	gnome	# with gnome1
#
Summary:	Tools for burning CDRs in Disk At Once mode
Summary(pl):	Narzêdzia do wypalania p³yt w trybie Disk At Once
Summary(pt_BR):	Cdrdao - Escreve CD-Rs de áudio em modo "disk-at-once"
Name:		cdrdao
Version:	1.1.7
Release:	4
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/cdrdao/%{name}-%{version}.src.tar.bz2
# Source0-md5: a85c0fa006ad3af64b76fd86b10b2ad4
Patch0:		%{name}-destdir.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-nolibs.patch
Patch3:		%{name}-gcdmaster-paths.patch
URL:		http://cdrdao.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_gnome:BuildRequires:	gnome-libs-devel >= 1.2.3}
%{?with_gnome:BuildRequires:	gnomemm-devel >= 1.1.17}
%{?with_gnome:BuildRequires:	gtkmm-devel >= 1.2.5}
BuildRequires:	lame-libs-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pccts >= 1.33MR33-6
BuildRequires:	pccts-antlr
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
%patch2 -p1
%patch3 -p1

%build
cd paranoia
%{__autoconf}
cd ..
%{__autoconf}
# false gtkmm-config path can be used to disable building of GNOME frontend
applnkdir=%{_applnkdir}; export applnkdir
PIXMAPS_DIR="%{_pixmapsdir}/gcdmaster"; export PIXMAPS_DIR
%configure \
	--with-pcctsbin=%{_bindir} \
	--with-pcctsinc=/usr/lib/pccts/h \
	%{?without_gnome:--with-gtkmm-exec-prefix=/}

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
%attr(755,root,root) %{_bindir}/cdrdao
%attr(755,root,root) %{_bindir}/toc2*
%dir %{_datadir}/cdrdao
%{_datadir}/cdrdao/drivers
%{_mandir}/man1/cdrdao.*

%if %{with gnome}
%files gcdmaster
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gcdmaster
%{_mandir}/man1/gcdmaster.*
%{_pixmapsdir}/*
%{_applnkdir}/Utilities/CD-RW/gcdmaster.desktop
%endif
