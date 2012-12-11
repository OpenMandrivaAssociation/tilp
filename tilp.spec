%define Werror_cflags %nil
%define oname tilp2

%define version 1.16
%define release %mkrel 0.1

%define libticables_version 1.3.3
%define libticalcs_version 1.1.7
%define libtifiles_version 1.1.5
%define	libticonv_version 1.1.3

Summary:	Communicate with TI graphing calculators
Name:		tilp
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Communications
URL:		http://tilp.sourceforge.net/
Epoch:		1
Source:		%{oname}-%{version}.tar.bz2
Requires:	libticables >= %{libticables_version}
Requires:	libticalcs >= %{libticalcs_version}
BuildRequires:	libticables-devel >= %{libticables_version}
Buildrequires:	libticalcs-devel >= %{libticalcs_version}
BuildRequires:	libtifiles-devel >= %{libtifiles_version}
BuildRequires:	libglade2.0-devel
BuildRequires:	jpeg-devel
BuildRequires:	groff-for-man
BuildRequires:	imagemagick
BuildRequires:  gettext-devel
BuildRoot:	%{_tmppath}/%{oname}-%{version}-%{release}-buildroot

%description
TiLP is a program for Texas Instruments' graphing calculators. It allows
PC to communicate with a TI calculator and transfer data between them.

%prep
%setup -q -n %{oname}-%{version}

%build
LDFLAGS="${LDFLAGS:- -export-dynamic}"
export LDFLAGS
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std \
    gnulocaledir=%{buildroot}%{_datadir}/locale \
    MKINSTALLDIRS="`pwd`/mkinstalldirs"

# menu and icon
mkdir -p %{buildroot}%{_liconsdir} \
         %{buildroot}%{_iconsdir} \
         %{buildroot}%{_miconsdir}
convert -geometry 48x48 help/logo_tilp.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 help/logo_tilp.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 help/logo_tilp.png %{buildroot}%{_miconsdir}/%{name}.png


# these files are to be merged into magic files for GNOME and KDE desktop
# install -m 644 desktop/gnome/gnome-vfs-mime-magic %{buildroot}%{_datadir}/%{name}/gnome-vfs-mime-magic
# install -m 644 desktop/kde/magic %{buildroot}%{_datadir}/%{name}/kde-magic

# remove files not bundled
rm -rf	%{buildroot}%{_libdir}/tilp/*.la \
	%{buildroot}%{_includedir}

%find_lang %{oname}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%triggerin -- gnome-mime-data
grep -q "\*\*TI" %{_sysconfdir}/gnome-vfs-mime-magic || \
  cat %{_datadir}/%{name}/gnome-vfs-mime-magic >> %{_sysconfdir}/gnome-vfs-mime-magic

%triggerin -- kdelibs-common
grep -q "\*\*TI" %{_datadir}/mimelnk/magic || \
  cat %{_datadir}/%{name}/kde-magic >> %{_datadir}/mimelnk/magic

%files -f %{oname}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README README.linux 
%doc RELEASE TODO
#%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/*
# %{_kde3_datadir}/%{oname}/*
%{_datadir}/%{oname}
%{_mandir}/man1/*
# %{_datadir}/application-registry/*.applications
# %{_datadir}/applications/*.desktop
# %{_datadir}/applnk/*/*/*.desktop
# %{_datadir}/mime-info/*
# %{_datadir}/mimelnk/application/*.desktop
%{_datadir}/applications/tilp.desktop
%{_datadir}/mime/packages/tilp.xml

%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png




%changelog
* Thu Jan 19 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.16-0.1mdv2012.0
+ Revision: 762281
- Upgrade to 1.16
- Upgrade to 1.16

* Tue Jul 13 2010 Zombie Ryushu <ryushu@mandriva.org> 1:1.14-0.1mdv2011.0
+ Revision: 551966
- Upgrade to 1.14
- import tilp


* Sat Mar 14 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.12-2mdv2009.1
+ Revision: 355057
- drop unapplied patches
- drop wrong libtifiles dep
- drop useless autotools suite rebuilding

* Sat Mar 07 2009 Zombie Ryushu <ryushu@mandriva.org> 1:1.12-1mdv2009.1
+ Revision: 351491
- Adjust build requires version numbers for underlying libraries
- Add Epoch
- Update to TILP2 1.12
- Work in Progress

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - Fix configure option to not use Qt4 libs if this is a Qt3 application

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Wed Jul 23 2008 Thierry Vignaud <tvignaud@mandriva.com> 6.81-3mdv2009.0
+ Revision: 242858
- rebuild
- drop old menu
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Jul 02 2007 Olivier Thauvin <nanardon@mandriva.org> 6.81-1mdv2008.0
+ Revision: 46878
- 6.81
- Import tilp



* Sun Jan 08 2006 Olivier Thauvin <nanardon@mandriva.org> 6.79-2mdk
- Fix #20033, as suggest by Pierre (Comment #1)
- Fix missing BuildRequires (Pierre also)

* Tue Jul 05 2005 Olivier Thauvin <nanardon@mandriva.org> 6.79-1mdk
- 6.79
- rediff patch1, patch2
- remove patch0, no longer need

* Sun May 30 2004 Abel Cheung <deaddog@deaddog.org> 6.72-1mdk
- New version
- Rediff P2, P3
- Inserts magic entry whenever new GNOME and KDE magic files are installed
- Use ImageMagick to convert icons

* Sat Oct 11 2003 Abel Cheung <deaddog@deaddog.org> 6.68-1mdk
- 6.68 (GTK 2 based)
- Merge everything back into one package, because:
  - the "libraries" are plugins
  - the "header files" are only for compiling bundled plugins, and
    completely useless otherwise
- Patch1: compile plugin without shared library version
- Redo Patch2 (Fix DESTDIR support)
- Patch3: Fix installation of plugin, and don't install test plugin

* Sat Apr 26 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 6.09-1mdk
- 6.08 or 6.09, depends what we trust on sourceforge
- buildrequires (stefan spam :)

* Mon Feb 10 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 6.04-1mdk
- 6.04
- -patch{0,1}; +patch2 (fix destdir)
- split lib/libdevel

* Fri Dec 27 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 5.34-3mdk
- rebuild for rpm and glibc

* Sun Nov 24 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 5.34-2mdk
- rebuild
- fix missing files

* Wed Sep 04 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 5.34-1mdk
- port to mdk
- 5.34
- add menu and icones

* Sun May  6 2001 Benjamin Gordon <ben@bxg.org>
- Updated to version 4.16

* Sat Mar 24 2001 Benjamin Gordon <ben@bxg.org>
- Updated to version 4.06

* Sun Feb 18 2001 Benjamin Gordon <ben@bxg.org>
- Updated to version 3.93
