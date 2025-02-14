%undefine _debugsource_packages
%bcond_with	allegro_unstable

Name:		atanks
Version:	6.6
Release:	1
Summary:	Scorched Earth game clone
License:	GPLv2+
Group:		Games/Arcade
Url:		https://atanks.sourceforge.net/
Source0:	http://downloads.sourceforge.net/sourceforge/atanks/atanks-%{version}.tar.gz
Source3:	%{name}-16.png
Source4:	%{name}-32.png
Source5:	%{name}-48.png
#Patch0:		atanks-5.4-link.patch
%if %with allegro_unstable
BuildRequires:	allegro-testing-devel
%else
BuildRequires:	allegro-devel
%endif

%description
This is Atomic Tanks, a multi-player game similar to Scorched Earth
which involves firing enormous weapons to try and destroy the other
tanks.

%prep
%autosetup -p1

%build
%make_build \
	CC="%{__cxx}" \
	OFLAGS="%{optflags}" \
	LFLAGS="%{ldflags} -L%{_libdir} -lX11 -lXext -lXcursor -lXpm -lxcb -lXrender -lXfixes -lXau -lXdmcp" \
	INSTALLDIR=%{_gamesdatadir}/%{name}

%install
%make_install \
	BINDIR=%{_gamesbindir} \
	INSTALLDIR=%{_gamesdatadir}/%{name}

# Icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/16x16/apps
mkdir -p %{buildroot}%{_iconsdir}/hicolor/32x32/apps

install -D -m 644 %{SOURCE3} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -D -m 644 %{SOURCE4} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png

%files
%doc Changelog README TODO
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/io.sourceforge.atanks.metainfo.xml
