# DO NOT MODIFY CONTENTS OF PACKAGE - AGAINST LICENSE AND MAKES IT UNDISTRIBUTABLE
# AND ALSO IT IS ALREADY STRIPPED.

%define		no_install_post_strip		1
%define		no_install_post_compress_docs	1
%define		no_install_post_chrpath		1
Summary:	Zend Optimizer - PHP code optimizer
Summary(pl.UTF-8):	Zend Optimizer - optymalizator kodu PHP
Name:		php%{?php_suffix}-ZendOptimizer
Version:	3.3.9
Release:	1
License:	Zend License, distributable only if unmodified and for free (see LICENSE)
Group:		Libraries
Source0:	http://downloads.zend.com/optimizer/3.3.9/ZendOptimizer-%{version}-linux-glibc23-i386.tar.gz
# Source0-md5:	150586c3af37fbdfa504cf142c447e57
Source1:	http://downloads.zend.com/optimizer/3.3.9/ZendOptimizer-%{version}-linux-glibc23-x86_64.tar.gz
# Source1-md5:	dd4a95e66f0bda61d0006195b2f42efa
URL:		http://www.zend.com/products/zend_optimizer
BuildRequires:	rpmbuild(macros) >= 1.344
BuildRequires:	tar >= 1:1.15.1
Requires(triggerpostun):	sed >= 4.0
Requires:	php%{?php_suffix}-common >= 4:5.0.4
Obsoletes:	ZendOptimizer
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zend Optimizer - PHP code optimizer.

%description -l pl.UTF-8
Zend Optimizer - optymalizator kodu PHP.

%prep
%setup -q -c

%ifarch %{ix86}
%{__tar} --strip-components=1 -zxf %{SOURCE0}
%endif
%ifarch %{x8664}
%{__tar} --strip-components=1 -zxf %{SOURCE1}
%endif

cat <<'EOF' > data/zendoptimizer.ini
; ZendOptimizer user settings.
[Zend]
zend_optimizer.optimization_level=15
EOF

cat <<'EOF' > data/pack.ini
; ZendOptimizer package settings. Overwritten with each upgrade.
; if you need to add options, edit %{name}.ini instead
[Zend]
zend_extension=%{_libdir}/Zend/ZendOptimizer.so
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/php%{?php_suffix}

install -D data/%{php_major_version}_%{php_minor_version}_x_comp/ZendOptimizer.so \
	 $RPM_BUILD_ROOT%{_libdir}/Zend/ZendOptimizer.so

install data/poweredbyoptimizer.gif $RPM_BUILD_ROOT%{_sysconfdir}/php%{?php_suffix}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/php%{?php_suffix}/conf.d
install data/zendoptimizer.ini $RPM_BUILD_ROOT/etc/php%{?php_suffix}/conf.d/zendoptimizer.ini
install data/pack.ini $RPM_BUILD_ROOT/etc/php%{?php_suffix}/conf.d/zendoptimizer_pack.ini

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ "$1" = "0" ]; then
	%php_webserver_restart
fi

%post
%php_webserver_restart
if [ "$1" = 1 ]; then
%banner -e %{name} <<EOF
Remember to read %{_docdir}/%{name}-%{version}/LICENSE.gz!
EOF
fi

%triggerpostun -- %{name} < 2.5.10a-0.20
if [ -f /etc/php%{?php_suffix}/php.ini ]; then
	cp -f /etc/php%{?php_suffix}/conf.d/ZendOptimizer.ini{,.rpmnew}
	sed -ne '/^\(zend_\|\[Zend\]\)/{/^zend_extension\(_manager\.optimizer\)\?\(_ts\)\?=/d;p}' /etc/php%{?php_suffix}/php.ini > /etc/php%{?php_suffix}/conf.d/ZendOptimizer.ini
	cp -f /etc/php%{?php_suffix}/php.ini{,.rpmsave}
	sed -i -e '/^\(zend_\|\[Zend\]\)/d' /etc/php%{?php_suffix}/php.ini
fi

%files
%defattr(644,root,root,755)
%doc README* EULA* LICENSE
%dir %{_libdir}/Zend
%attr(755,root,root) %{_libdir}/Zend/ZendOptimizer.so
%config(noreplace) %verify(not md5 mtime size) /etc/php%{?php_suffix}/conf.d/zendoptimizer.ini
%config %verify(not md5 mtime size) /etc/php%{?php_suffix}/conf.d/zendoptimizer_pack.ini
/etc/php%{?php_suffix}/poweredbyoptimizer.gif
