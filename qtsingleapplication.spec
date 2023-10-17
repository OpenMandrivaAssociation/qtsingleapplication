%global commit0 777e95ba69952f11eaec0adfb0cb987fabcdecb3
%global _qt5_headerdir %{_includedir}/qt5
%global _qt5_archdatadir %{_libdir}/qt5

Summary:    Qt library to start applications only once per user
Name:       qtsingleapplication
Version:    2.6.1
Release:    35

License:    GPLv3 or LGPLv2 with exceptions
URL:        http://doc.qt.digia.com/solutions/4/qtsingleapplication/qtsingleapplication.html
Source0:    https://github.com/qtproject/qt-solutions/archive/%{commit0}.tar.gz#/%{name}-%{commit0}.tar.gz
# Proposed upstream in https://codereview.qt-project.org/#/c/92417/
Source1:    qtsingleapplication.prf
# Proposed upstream in https://codereview.qt-project.org/#/c/92416/
Source2:    qtsinglecoreapplication.prf
# Proposed upstream in https://codereview.qt-project.org/#/c/92411/
Source3:    LICENSE.GPL3
# Proposed upstream in https://codereview.qt-project.org/#/c/92411/
Source4:    LICENSE.LGPL
# Proposed upstream in https://codereview.qt-project.org/#/c/92411/
Source5:    LGPL_EXCEPTION

# Proposed upstream in https://codereview.qt-project.org/#/c/92416/
Patch0:     qtsingleapplication-build-qtsinglecoreapplication.patch
# Proposed upstream in https://codereview.qt-project.org/#/c/92415/
Patch1:     qtsingleapplication-remove-included-qtlockedfile.patch

# Features for unbundling in Qupzilla, https://github.com/QupZilla/qupzilla/issues/1503
Patch2:     qtsingleapplication-qupzilla.patch

BuildRequires: qt5-qtbase-devel
BuildRequires: qtlockedfile-qt5-devel

%description
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

The QtSingleApplication class provides an interface to detect a running
instance, and to send command strings to that instance.

%package qt5
Summary:    Qt5 library to start applications only once per user

%description qt5
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

This is a special build against Qt5.

%package qt5-devel
Summary:    Development files for %{name}-qt5
Requires:   %{name}-qt5 = %{version}-%{release}
Requires:   qt5-qtbase-devel

%description qt5-devel
This package contains libraries and header files for developing applications
that use QtSingleApplication with Qt5.

%package -n qtsinglecoreapplication-qt5
Summary:    Qt library to start applications only once per user (Qt5)

%description -n qtsinglecoreapplication-qt5
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

For console (non-GUI) applications, the QtSingleCoreApplication variant
is provided, which avoids dependency on QtGui.

This is a special build against Qt5.

%package -n qtsinglecoreapplication-qt5-devel
Summary:    Development files for qtsinglecoreapplication-qt5
Requires:   qtsinglecoreapplication-qt5 = %{version}-%{release}
Requires:   qt5-qtbase-devel

%description -n qtsinglecoreapplication-qt5-devel
This package contains libraries and header files for developing applications
that use QtSingleCoreApplication.


%prep
%setup -qn qt-solutions-%{commit0}
%patch0 -p0
%patch1 -p0
%patch2 -p1
# use versioned soname
sed -i "s,head,%(echo '%{version}' |sed -r 's,(.*)\..*,\1,'),g" common.pri

mkdir licenses
cp -p %{SOURCE3} %{SOURCE4} %{SOURCE5} licenses

# We already disabled bundling this external library.
# But just to make sure:
rm -rf ../qtlockedfile/
sed -i 's,qtlockedfile\.h,QtSolutions/\0,' src/qtlocalpeer.h
rm src/{QtLocked,qtlocked}*

mkdir qt5
cp -p %{SOURCE1} %{SOURCE2} qt5
sed -i -r 's,-lQt,\05,' qt5/qtsingleapplication.prf
sed -i -r 's,-lQt,\05,' qt5/qtsinglecoreapplication.prf

# additional header needed for Qt5.5
sed -i -r 's,.include,\0 <QtCore/QDataStream>\n\0,' src/qtlocalpeer.h


%build
# Does not use GNU configure
./configure -library
%{qmake_qt5}
%make_build


%install
# libraries
mkdir -p %{buildroot}%{_libdir}
cp -a lib/* %{buildroot}%{_libdir}
chmod 755 %{buildroot}%{_libdir}/*.so*

# headers
mkdir -p %{buildroot}%{_qt5_headerdir}/QtSolutions
cp -ap \
    src/qtsingleapplication.h \
    src/QtSingleApplication \
    src/qtsinglecoreapplication.h \
    src/QtSingleCoreApplication \
    %{buildroot}%{_qt5_headerdir}/QtSolutions
mkdir -p %{buildroot}%{_qt5_headerdir}

mkdir -p %{buildroot}%{_qt5_archdatadir}/mkspecs/features
install -p -m644 qt5/*.prf %{buildroot}%{_qt5_archdatadir}/mkspecs/features


%files
%license licenses/*
%doc README.TXT

%files qt5
%license licenses/*
%doc README.TXT
# Caution! Unversioned .so file goes into -devel
%{_qt5_libdir}/libQt5*SingleApplication*.so.*

%files qt5-devel
%doc doc/html/ examples/
%{_qt5_libdir}/libQt5*SingleApplication*.so
%dir %{_qt5_headerdir}/QtSolutions/
%{_qt5_headerdir}/QtSolutions/QtSingleApplication
%{_qt5_headerdir}/QtSolutions/%{name}.h
%{_qt5_archdatadir}/mkspecs/features/qtsingleapplication.prf

%files -n qtsinglecoreapplication-qt5
%license licenses/*
# Caution! Unversioned .so file goes into -devel
%{_qt5_libdir}/libQt5*SingleCoreApplication*.so.*

%files -n qtsinglecoreapplication-qt5-devel
%{_qt5_libdir}/libQt5*SingleCoreApplication*.so
%dir %{_qt5_headerdir}/QtSolutions/
%{_qt5_headerdir}/QtSolutions/QtSingleCoreApplication
%{_qt5_headerdir}/QtSolutions/qtsinglecoreapplication.h
%{_qt5_archdatadir}/mkspecs/features/qtsinglecoreapplication.prf
