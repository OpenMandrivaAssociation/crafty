%define version 19.19
%define release %mkrel 5

Summary:	A free chess program, plays decent game of chess
Name:		crafty
Version:	%{version}
Release:	%{release}
License:	Freeware
Group:		Games/Boards
URL:		http://www.cis.uab.edu/info/faculty/hyatt/hyatt.html
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source:		ftp://ftp.cis.uab.edu/pub/hyatt/source/%{name}-%{version}.tar.bz2
Source10:	%{name}.sh.bz2
Source11:	%{name}-opening-book.tar.bz2
Source12:	crafty.txt.bz2
Source20:	crafty.6.bz2
Source21:	crafty.rc.5.bz2

# 1-20: Mandriva patches
# (Abel) Makefile linux-sparc target support, and don't
# add smp and i686 flags in default build
Patch0:		crafty-19.19-makefile.patch
# (Abel) read help file in shared folder, not $cwd
Patch1:		crafty-19.19-help-path.patch.bz2
# (Abel) Fix for gcc 4.0
Patch2:		crafty-19.19-gcc40.patch.bz2
# (Abel) read computer and small opening book from shared folder
Patch3:		crafty-19.19-globalbookpath.patch.bz2


# 21-40: Debian patches
Patch21:	crafty-19.19-alpha.patch.bz2
Patch22:	crafty-19.19-security-flaw.patch.bz2
# Attempt to read global config (/etc/crafty.rc) when personal config
# (~/.craftyrc) is not found
Patch23:	crafty-19.19-global-config.patch.bz2
# Other cleanup
Patch24:	crafty-19.19-va-arg.patch.bz2

# 41- : Other generic patches
# (Abel) Fix some compiler warnings
Patch41:	crafty-19.19-warnings.patch.bz2
# (Abel) Split book initialization into function, otherwise using
#        "book on" won't initialize it properly
Patch42:	crafty-19.19-initialize-book.patch.bz2
# (Abel) Plug segfaults (though they are not architectually correct
#        fixes, just avoiding problem for now)
Patch43:	crafty-19.19-segfault.patch.bz2
# (Abel) Plug some memory leaks
Patch44:	crafty-19.19-memleak.patch.bz2
# (Abel) strcpy -> strncpy, sprintf -> snprintf
Patch45:	crafty-19.19-overflow.patch.bz2

Provides:	chessengine

%description
Crafty is a chess program written by Bob Hyatt <hyatt at cis.uab.edu>.
It is a direct descendent of Cray Blitz, the World Computer Champion
from 1983 to 1989.

It comes with a text interface like gnuchess do. If you want a graphical
interface, you can install GUI chessboards such as xboard and eboard.

Crafty is based on the classic BITMAP approach to representing the chess
board, but uses a unique methodology called "rotated bitmaps" to
significantly improve the performance of the chess engine.

%prep
%setup -q
%patch0 -p1 -b .opt
%patch1 -p1 -b .help
%patch2 -p1 -b .gcc40
%patch3 -p1 -b .bookpath

%patch21 -p1 -b .alpha
%patch22 -p1 -b .security
%patch23 -p1 -b .config
%patch24 -p1 -b .cleanup

%patch41 -p1 -b .warnings
%patch42 -p1 -b .init-book
%patch43 -p1 -b .segfault
%patch44 -p1 -b .memleak
%patch45 -p1 -b .overflow

bzcat %{SOURCE12} > crafty.txt

%build
%{?cpus: export NCPUS=%cpus}

%ifarch x86_64 amd64
make linux-amd64 OPTIMIZE='-ffast-math %optflags'
%else

%ifarch alpha
make linux-alpha OPTIMIZE='-ffast-math %optflags'
%else

%ifarch i686
make linux-i686 OPTIMIZE='-march=i686 -mtune=pentium4 -ffast-math -fno-gcse %optflags'
%else

%ifarch pentium3
make linux-i686 OPTIMIZE='-march=pentium3 -mfpmath=sse -ffast-math -fno-gcse %optflags'
%else

%ifarch pentium4
make linux-i686 OPTIMIZE='-march=pentium4 -mfpmath=sse2 -ffast-math -fno-gcse %optflags'
%else

%ifarch i586
make linux OPTIMIZE='-ffast-math %optflags'
%else

make linux-generic OPTIMIZE='-ffast-math %optflags'
%endif
%endif
%endif
%endif
%endif
%endif

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_gamesbindir}
install -m 755 crafty %{buildroot}/%{_gamesbindir}/crafty.real

bzcat %{SOURCE10} > %{buildroot}/%{_gamesbindir}/crafty
chmod 755 %{buildroot}/%{_gamesbindir}/crafty

install -D -m 644 crafty.hlp %{buildroot}%{_gamesdatadir}/crafty/crafty.hlp
tar --bzip2 -xf %{SOURCE11} -C %{buildroot}%{_gamesdatadir}/crafty/

# manpages
mkdir -p %{buildroot}%{_mandir}/man{5,6}
bzip2 -dc %{SOURCE20} > %{buildroot}%{_mandir}/man6/crafty.6
bzip2 -dc %{SOURCE21} > %{buildroot}%{_mandir}/man5/crafty.rc.5

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root)
%doc crafty.txt
%{_gamesbindir}/*
%{_gamesdatadir}/crafty
%{_mandir}/man?/*

