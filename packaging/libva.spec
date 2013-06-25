%bcond_with wayland 
%bcond_with mesa

Name:           libva
Version:        1.1.1
Release:        0
License:        MIT
Summary:        Video Acceleration (VA) API for Linux
Url:            http://freedesktop.org/wiki/Software/vaapi
Group:          Multimedia/Video
Source:         %{name}-%{version}.tar.bz2
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  mesa-devel
BuildRequires:  pkg-config
BuildRequires:  xz
%if %{with mesa}
BuildRequires: pkgconfig(gl)
%else
BuildRequires: pkgconfig(gles11)
%endif
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xv)
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
Requires:       pkgconfig(x11)
Requires:       pkgconfig(xfixes)

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
%autogen
%configure --enable-dummy-driver \
           --enable-dummy-backend \
           --enable-glx \
           --enable-egl \
%if %{with wayland}
           --enable-wayland \
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
%{_bindir}/putsurface
%{_bindir}/loadjpeg
%if %{with wayland}
%{_bindir}/putsurface_wayland
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
%{_libdir}/libva-x11.so.*
%{_libdir}/libva-glx.so.*
%{_libdir}/libva-egl.so.*
%if %{with wayland}
%{_libdir}/libva-wayland.so.*
%endif
%{_libdir}/libva-drm.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libva.so
%{_libdir}/libva-tpi.so
%{_libdir}/libva-x11.so
%{_libdir}/libva-glx.so
%{_libdir}/libva-egl.so
%if %{with wayland}
%{_libdir}/libva-wayland.so
%endif
%{_libdir}/libva-drm.so
%{_includedir}/va
%{_libdir}/pkgconfig/libva*.pc

%changelog
