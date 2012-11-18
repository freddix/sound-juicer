Summary:	CD ripper
Name:		sound-juicer
Version:	3.5.0
Release:	1
License:	GPL v2+
Group:		X11/Aplications/Multimedia
Source0:	http://ftp.gnome.org/pub/GNOME/sources/sound-juicer/3.5/%{name}-%{version}.tar.xz
# Source0-md5:	68fdb3b2530f4b19f7ac220690905e73
Patch0:		%{name}-musicbrainz5.patch
URL:		http://www.burtonini.com/blog/computers/sound-juicer/
BuildRequires:	GConf-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	brasero-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	gtk+-devel
BuildRequires:	intltool
BuildRequires:	libcanberra-gtk-devel
BuildRequires:	libcdio-devel
BuildRequires:	libdiscid-devel
BuildRequires:	libmusicbrainz5-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
Requires(post,preun):	GConf
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	rarian
Requires:	gstreamer-plugins-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sound Juicer, a CD ripping tool using GTK+ and GStreamer.

%prep
%setup -q
#%patch0 -p1

# kill gnome common deps
sed -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.in

%build
%{__gnome_doc_prepare}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules		\
	--disable-schemas-install	\
	--disable-scrollkeeper
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw,ha,ig,la}

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install sound-juicer.schemas
%scrollkeeper_update_post
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall sound-juicer.schemas

%postun
%scrollkeeper_update_postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_desktopdir}/*
%{_iconsdir}/hicolor/*/apps/*
%{_sysconfdir}/gconf/schemas/sound-juicer.schemas

%{_mandir}/man1/sound-juicer.1*

