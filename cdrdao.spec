# NOTE:		
#	Currently this package does not contain X interface. This is due to
#	the fact, that it doesn't compile with current version of gtkmm. I
#	have asked author if he is going to update this program, but I've got
#	no answer yet.
Summary:	Tools for burning CDRs in Disk At Once mode
Summary(pl):	Narzêdzia do wypalania p³yt w trybie Disk At Once
Name:		cdrdao
Version:	1.1.3
Release:	1
Group:		Utilities/System
Group(pl):	Narzêdzia/System
License:	GPL
Source0:	http://www.ping.de/sites/daneb/%{name}-%{version}.src.tar.gz
Patch0:		%{name}-destdir.patch
Patch1:		%{name}-opt.patch
BuildRequires:	libstdc++-devel
BuildRequires:	libsigc++-devel
BuildRequires:	pccts-devel
# Required by frontend.
#BuildRequires:	gtk+-devel
#BuildRequires:	gtkmm-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cdrdao records audio and data CD-Rs in Disk At Once mode. This mode
gives much better control over contents of CD.

%description -l pl
Cdrdao zapisuje p³ytki audio i z danymi w trybie Disk At Once. W tym
trybie masz znacznie wiêksz± kontrolê nad zawarto¶ci± p³ytki.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1

%build
#autoheader;autoconf;automake; 
(cd paranoia ; autoconf)
#CFLAGS="-I%{_prefix}/X11R6/includes"
%configure \
	--with-pcctsbin=%{_bindir} \
	--with-pcctsinc=%{_includedir}/pccts \
	--x-includes=%{_prefix}/X11R6/includes
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	COPYING CREDITS README* Release*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_mandir}/*/*
%attr(755,root,root) %{_bindir}/*
%doc *.gz
