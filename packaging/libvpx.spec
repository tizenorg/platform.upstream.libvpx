Name:           libvpx
Version:        1.1.0
Release:        0
%define patchlevel %{nil}
License:        BSD-3-Clause ; GPL-2.0+
Summary:        VP8 codec library
Url:            http://www.webmproject.org/
Group:          Productivity/Multimedia/Other
Source0:        http://webm.googlecode.com/files/%{name}-v%{version}%{patchlevel}.tar.bz2
BuildRequires:  yasm

%description
WebM is an open, royalty-free, media file format designed for the web.

WebM defines the file container structure, video and audio formats.
WebM files consist of video streams compressed with the VP8 video codec
and audio streams compressed with the Vorbis audio codec.
The WebM file structure is based on the Matroska container.

%package -n vpx-tools
License:        BSD-3-Clause ; GPL-2.0+
Summary:        VP8 codec library - Utilities
Group:          Productivity/Multimedia/Other

%description -n vpx-tools
This package contains utilities around the vp8 codec sdk.

WebM is an open, royalty-free, media file format designed for the web.

WebM defines the file container structure, video and audio formats.
WebM files consist of video streams compressed with the VP8 video codec
and audio streams compressed with the Vorbis audio codec.
The WebM file structure is based on the Matroska container.
%package devel
License:        BSD-3-Clause ; GPL-2.0+
Summary:        VP8 codec library - Development headers
Group:          Development/Languages/C and C++
Requires:       %{name} = %{version}

%description devel
Development headers and library

WebM is an open, royalty-free, media file format designed for the web.

WebM defines the file container structure, video and audio formats.
WebM files consist of video streams compressed with the VP8 video codec
and audio streams compressed with the Vorbis audio codec.
The WebM file structure is based on the Matroska container.

%prep
%setup -q -n %name-v%version%patchlevel

%build
cd build
export CFLAGS="%{optflags}"
# It is only an emulation of autotools configure; the macro does not work

# libvpx default enable NEON support on ARMv7, unfortunately some ARMv7
# CPU doesn't have NEON, e.g. NVIDIA Tegra 2.
# So, we still set -mfpu=neon when build libvpx rpm, but also enable
# runtime-cpu-detect for runtime detect NEON.
../configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-debug \
    --enable-shared \
%ifarch armv7l armv7hl
    --target=armv7-linux-gcc \
    --enable-runtime-cpu-detect \
%endif
    --enable-pic
make %{?_smp_mflags}

%install
cd build
%make_install

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files -n vpx-tools
%defattr(-,root,root)
%{_bindir}/*

%files 
%defattr(-, root, root)
%license LICENSE
%{_libdir}/libvpx.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/vpx/
%{_libdir}/pkgconfig/vpx.pc
%{_libdir}/libvpx.so
