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

%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png


