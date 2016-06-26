#
# Conditional build:
%bcond_without	boost		#
%bcond_with	gtest		#
%bcond_without	protobuf		#
%bcond_without	ssl		#
%bcond_with	v8		#
%bcond_with	python		#

Summary:	Command line shell and scripting environment for MySQL
Name:		mysql-shell
Version:	1.0.4
Release:	0.1
License:	GPL v2
Source0:	https://cdn.mysql.com/Downloads/%{name}-%{version}-src.tar.gz
# Source0-md5:	b8e721b11a98e74539747204ae08ac64
Group:		Applications/Databases
URL:		http://dev.mysql.com/doc/refman/en/mysql-shell.html
%{?with_boost:BuildRequires:  boost-devel >= 1.42}
BuildRequires:	cmake >= 2.8
#BuildRequires:	libedit-devel  FIXME only if -DWITH_EDITLINE=system
%{?with_protobuf:BuildRequires:  protobuf-devel}
BuildRequires:	python-devel
BuildRequires:	mysql-devel
BuildRequires:	openssl-devel
#BuildRequires:  v8-devel
#BuildRequires:  v8-python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The MySQL Shell is an interactive JavaScript, Python, or SQL interface
supporting development and administration for the MySQL Server and is
a component of the MySQL Server. You can use the MySQL Shell to
perform data queries and updates as well as various administration
operations.

The MySQL Shell provides:
- Both Interactive and Batch operations
- JavaScript, Python, and SQL language modes
- Document and Relational Models
- CRUD Document and Relational APIs via scripting
- Traditional Table, JSON, Tab Separated output results formats
- Stored Sessions
- MySQL Standard and X Protocols

%prep
%setup -q -n %{name}-%{version}-src

%build
install -d build
cd build

%cmake \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DMYSQLCLIENT_STATIC_LINKING=OFF \
%if %{with v8}
	-DV8_INCLUDE_DIR=/usr/include/v8 \
	-DV8_LIB_DIR=%{_libdir} \
%else
	-DHAVE_V8=OFF \
%endif
	-DWITH_SSL=system \
%if %{with boost}
	-DBOOST_ROOT=ON \
	-DBoost_NO_SYSTEM_PATHS:BOOL=TRUE \
%endif
%if %{with protobuf}
	-DWITH_PROTOBUF=ON \
%endif
%if %{with gtest}
	-DWITH_TESTS=ON \
	-DWITH_GTEST=ON \
%endif
%if %{with python}
	-DHAVE_PYTHON=1 \
%else
	-DHAVE_PYTHON=OFF \
%endif
	..

# Shared linking don't work
# -DMYSQLCLIENT_STATIC_LINKING=ON \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT%{_includedir}
rm $RPM_BUILD_ROOT%{_prefix}/lib/*.{so,a}
rm $RPM_BUILD_ROOT%{_datadir}/mysqlsh/{COPYING.txt,README}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/mysqlsh
%{_mandir}/man1/mysqlsh.1*
%{_datadir}/mysqlsh/modules/js/mysql.js
%{_datadir}/mysqlsh/modules/js/mysqlx.js
