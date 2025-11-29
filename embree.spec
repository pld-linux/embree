Summary:	High Performance Ray Tracing Kernels
Name:		embree
Version:	4.4.0
Release:	1
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/embree/embree/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	86bdca35c68b8016681dc5de102a3fa1
Patch0:		cmake-pld.patch
URL:		https://www.embree.org/
BuildRequires:	OpenGL-devel
BuildRequires:	cmake
BuildRequires:	libjpeg-devel
BuildRequires:	tbb-devel
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Intel® Embree is a collection of high-performance ray tracing kernels,
developed at Intel. The target users of Intel® Embree are graphics
application engineers who want to improve the performance of their
photo-realistic rendering application by leveraging Embree's
performance-optimized ray tracing kernels. The kernels are optimized
for the latest Intel® processors with support for SSE, AVX, AVX2, and
AVX-512 instructions. Intel® Embree supports runtime code selection to
choose the traversal and build algorithms that best matches the
instruction set of your CPU. We recommend using Intel® Embree through
its API to get the highest benefit from future improvements.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%prep
%setup -q
%patch -P0 -p1

%build
mkdir -p build
cd build
%cmake ../ \
	-DEMBREE_MAX_ISA=SSE4.2 \
	-DEMBREE_IGNORE_CMAKE_CXX_FLAGS=OFF \
	-DCMAKE_CXX_STANDARD=17 \
	-DEMBREE_ISPC_SUPPORT=OFF \
	-DEMBREE_TUTORIALS=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_mandir}/man3/
for f in *.4embree4 ; do
	%{__mv} "$f" "$(basename "$f" .4embree4).3embree4"
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md SECURITY.md
%attr(755,root,root) %{_libdir}/libembree4.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libembree4.so
%{_includedir}/%{name}4
%{_libdir}/cmake/%{name}-%{version}
%{_mandir}/man3/*.3embree4*
