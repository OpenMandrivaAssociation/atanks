%bcond_with     allegro_unstable

Name:           atanks
Version:        5.3
Release:        %mkrel 1
Summary:        Scorched Earth game clone
License:        GPLv2+
Group:          Games/Arcade
Url:            http://atanks.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sourceforge/atanks/atanks-%{version}.tar.gz
Source3:        %{name}-16.png
Source4:        %{name}-32.png
Source5:        %{name}-48.png
Patch0:		atanks-5.3-link.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
%if %with allegro_unstable
BuildRequires:  allegro-testing-devel
%else
BuildRequires:  allegro-devel
%endif

%description
This is Atomic Tanks, a multi-player game similar to Scorched Earth
which involves firing enormous weapons to try and destroy the other
tanks.

%prep
%setup -q
%apply_patches

%build
%make \
	CC="%{__cxx}" \
	OFLAGS="%{optflags}" \
	LDFLAGS="%{ldflags}" \
	INSTALLDIR=%{_gamesdatadir}/%{name}

%install
%{__rm} -rf %{buildroot}

%makeinstall_std \
	BINDIR=%{_gamesbindir} \
	INSTALLDIR=%{_gamesdatadir}/%{name}

%{__perl} -pi -e "s/\r$//g" %{buildroot}%{_gamesdatadir}/%{name}/tanks.txt

# Fix icon in .desktop file
%{__perl} -pi -e "s/%{name}.png/%{name}/g" %{buildroot}%{_datadir}/applications/%{name}.desktop

# Icons
%{__mkdir_p} %{buildroot}%{_iconsdir}/hicolor/16x16/apps
%{__mkdir_p} %{buildroot}%{_iconsdir}/hicolor/32x32/apps

%{__install} -D -m 644 %{SOURCE3} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{__install} -D -m 644 %{SOURCE4} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png



%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changelog README TODO
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop

