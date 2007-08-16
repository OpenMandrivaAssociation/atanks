%bcond_with     allegro_unstable

Name:           atanks
Version:        2.5
Release:        %mkrel 1
Summary:        Scorched Earth game clone
License:        GPL
Group:          Games/Arcade
Url:            http://atanks.sourceforge.net/
Source0:        http://internap.dl.sourceforge.net/sourceforge/atanks/atanks-%{version}.tar.gz
Source3:        %{name}-16.png
Source4:        %{name}-32.png
Source5:        %{name}-48.png
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
%setup -q -n %{name}

%build
%{make} CC="%{__cxx}" OFLAGS="%{optflags}" FLAGS="-DLINUX -DVERSION=\\\"\${VERSION}\\\" -DDATA_DIR=\\\"%{_gamesdatadir}/%{name}\\\""

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}{%{_gamesbindir},%{_gamesdatadir}/%{name}}
%{__cp} -a %{name} %{buildroot}%{_gamesbindir}
%{__cp} -a *.dat %{buildroot}%{_gamesdatadir}/%{name}
%{__cp} -a *.txt %{buildroot}%{_gamesdatadir}/%{name}

%{__perl} -pi -e "s/\r$//g" %{buildroot}%{_gamesdatadir}/%{name}/tanks.txt

%{__chmod} 644 %{buildroot}%{_gamesdatadir}/%{name}/*

# Menu
%{__mkdir_p} %{buildroot}{%{_menudir},%{_liconsdir},%{_iconsdir},%{_miconsdir}}

%{__install} -D -m 644 %{SOURCE3} %{buildroot}%{_miconsdir}/%{name}.png
%{__install} -D -m 644 %{SOURCE4} %{buildroot}%{_iconsdir}/%{name}.png
%{__install} -D -m 644 %{SOURCE5} %{buildroot}%{_liconsdir}/%{name}.png

%{__install} -d -m 755 %{buildroot}%{_menudir}
%{__cat} >%{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}):\
    command="%{_gamesbindir}/%{name}"\
    title="Atanks"\
    longtitle="A worms clone"\
    needs="x11"\
    section="More Applications/Games/Arcade"\
    icon="%{name}.png"\
    xdg="true"
EOF

%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{__cat} > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=%{Summary}
Exec=%{name} -c
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Games-Arcade;Game;ArcadeGame;
EOF

%post
%{update_menus}

%postun
%{clean_menus}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README TODO BUGS Changelog
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_menudir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*