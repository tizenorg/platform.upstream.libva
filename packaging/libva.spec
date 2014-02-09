%bcond_with wayland 
%bcond_with mesa
%bcond_with x

Name:           libva
Version:        1.2.1
Release:        0
License:        MIT
Summary:        Video Acceleration (VA) API for Linux
Url:            http://freedesktop.org/wiki/Software/vaapi
Group:          Multimedia/Video
Source:         %{name}-%{version}.tar.bz2
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  pkg-config
BuildRequires:  xz
%if %{with mesa}
BuildRequires:  mesa-devel
%else
BuildRequires: pkgconfig(glesv2)
BuildRequires:  pkgconfig(egl)
%endif
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libudev)
%if %{with x}
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xv)
%endif
%if %{with wayland}
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-client)
%endif
ExclusiveArch:  %ix86 x86_64

%description
The libva library implements the Video Acceleration (VA) API for Linux.
The library loads a hardware dependendent driver.

%package devel
Summary:        Video Acceleration (VA) API for Linux -- development files
Group:          Development/Libraries
Requires:       libva = %{version}
Requires:       pkgconfig(gl)
Requires:       pkgconfig(libdrm)
%if %{with x}
Requires:       pkgconfig(x11)
Requires:       pkgconfig(xfixes)
%endif

%description devel
The libva library implements the Video Acceleration (VA) API for Linux.
The library loads a hardware dependendent driver.

This package provides the development environment for libva.

%package -n vaapi-tools
Summary:        Video Acceleration (VA) API for Linux
Group:          Multimedia/Video

%description -n vaapi-tools
The libva library implements the Video Acceleration (VA) API for Linux.
The library loads a hardware dependendent driver.

This is a set of tools around vaapi livrary.

%package -n vaapi-dummy-driver
Summary:        Video Acceleration (VA) API for Linux
Group:          Multimedia/Video

%description -n vaapi-dummy-driver
The libva library implements the Video Acceleration (VA) API for Linux.
The library loads a hardware dependendent driver.

This contains the dummy driver.

%prep
%setup -q

%build
# --enable-x11 set to no explicitly, otherwise it will mislead libva build when other package brings in X11 lib
%autogen
%configure --enable-dummy-driver \
           --enable-dummy-backend \
%if %{with mesa} && %{with x}
           --enable-glx \
%endif
           --enable-egl \
%if %{with wayland}
           --enable-wayland \
%endif
%if !%{with x}
        --enable-x11=no \
%endif
           --with-drivers-path=%{_libdir}/dri
make %{?_smp_mflags}

%install
%make_install
grep -r include %{buildroot}%{_includedir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n vaapi-tools
%defattr(-,root,root,-)
%{_bindir}/vainfo
%{_bindir}/avcenc
%{_bindir}/h264encode
%{_bindir}/mpeg2vldemo
%{_bindir}/mpeg2vaenc
%if %{with x}
%{_bindir}/putsurface
%endif
%{_bindir}/loadjpeg
%if %{with wayland}
# %{_bindir}/putsurface_wayland
%endif

%files -n vaapi-dummy-driver
%defattr(-,root,root,-)
%dir %{_libdir}/dri
%{_libdir}/dri/dummy_drv_video.so

%files
%defattr(-, root, root)
%license COPYING
%{_libdir}/libva.so.*
%{_libdir}/libva-tpi.so.*
%if %{with x}
%{_libdir}/libva-x11.so.*
%endif
%if %{with mesa} && %{with x}
    %{_libdir}/libva-glx.so.*
%endif
%{_libdir}/libva-egl.so.*
%if %{with wayland}
%{_libdir}/libva-wayland.so.*
%endif
%{_libdir}/libva-drm.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libva.so
%{_libdir}/libva-tpi.so
%if %{with x}
%{_libdir}/libva-x11.so
%endif
%if %{with mesa} && %{with x}
    %{_libdir}/libva-glx.so
%endif
%{_libdir}/libva-egl.so
%if %{with wayland}
%{_libdir}/libva-wayland.so
%endif
%{_libdir}/libva-drm.so
%{_includedir}/va
%{_libdir}/pkgconfig/libva*.pc

%changelog
