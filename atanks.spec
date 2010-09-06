%bcond_with     allegro_unstable

Name:           atanks
Version:        4.7
Release:        %mkrel 1
Summary:        Scorched Earth game clone
License:        GPLv2+
Group:          Games/Arcade
Url:            http://atanks.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sourceforge/atanks/atanks-%{version}.tar.gz
Source3:        %{name}-16.png
Source4:        %{name}-32.png
Source5:        %{name}-48.png
Patch1:		atanks-4.5-install.patch
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
%patch1 -p1 -b .install

%build
%{make} \
    CC="%{__cxx}" OFLAGS="%{optflags}" INSTALLDIR=%_gamesdatadir/%name

%install
%{__rm} -rf %{buildroot}

make install BINDIR=%buildroot%_gamesbindir INSTALLDIR=%buildroot%_gamesdatadir/%name

%{__perl} -pi -e "s/\r$//g" %{buildroot}%{_gamesdatadir}/%{name}/tanks.txt

%{__chmod} 644 %{buildroot}%{_gamesdatadir}/%{name}/*
%{__chmod} 755 %{buildroot}%{_gamesdatadir}/%{name}/*/

# Menu
%{__mkdir_p} %{buildroot}{%{_menudir},%{_liconsdir},%{_iconsdir},%{_miconsdir}}

%{__install} -D -m 644 %{SOURCE3} %{buildroot}%{_miconsdir}/%{name}.png
%{__install} -D -m 644 %{SOURCE4} %{buildroot}%{_iconsdir}/%{name}.png
%{__install} -D -m 644 %{SOURCE5} %{buildroot}%{_liconsdir}/%{name}.png

%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{__cat} > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=Scorched Earth game clone
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc Changelog COPYING README TODO
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*
