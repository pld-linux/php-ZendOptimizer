# DO NOT MODIFY CONTENTS OF PACKAGE - AGAINST LICENSE AND MAKES IT UNDISTRIBUTABLE
# AND ALSO IT IS ALREADY STRIPPED.

%define		no_install_post_strip		1
%define		no_install_post_compress_docs	1
%define		no_install_post_chrpath		1
Summary:	Zend Optimizer - PHP code optimizer
Summary(pl):	Zend Optimizer - optymalizator kodu PHP
Name:		ZendOptimizer
Version:	2.5.10a
Release:	0.11
License:	Zend License, distributable only if unmodified and for free (see LICENSE)
Group:		Libraries
Source0:	http://downloads.zend.com/optimizer/2.5.10/%{name}-%{version}-linux-glibc21-i386.tar.gz
# NoSource0-md5:	3064cb6d33f0d4800cf84b8a5521cd48
Source1:	http://downloads.zend.com/optimizer/2.5.10/%{name}-%{version}-linux-glibc23-x86_64.tar.gz
# NoSource1-md5:	6d7e50b1875fb77eff7d0cc6ff45db32
NoSource:	0
NoSource:	1
URL:		http://www.zend.com/zend/optimizer.php
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	tar >= 1:1.15.1
Requires(post):	grep >= 2:2.5.1
Requires(post):	sed >= 4.0.0
# circular dependency, so ones upgraded are forced to choose php and
# ones that want to install specific for specific version need not to
# install ZendOptimizer separately
Requires:	ZendOptimizer(php)
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zend Optimizer - PHP code optimizer.

%description -l pl
Zend Optimizer - optymalizator kodu PHP.

%package -n php4-%{name}
Summary:	Zend Optimizer for PHP 4.x.
Group:		Libraries
Requires:	ZendOptimizer = %{version}-%{release}
Requires:	php4 >= 3:4.0.6
Provides:	ZendOptimizer(php)

%description -n php4-%{name}
Zend Optimizer for PHP 4.x.

%package -n php-%{name}
Summary:	Zend Optimizer for PHP 5.x.
Group:		Libraries
Requires:	ZendOptimizer = %{version}-%{release}
Requires:	php >= 4:5.0.0
Provides:	ZendOptimizer(php)

%description -n php-%{name}
Zend Optimizer for PHP 5.x.

%prep
%setup -q -c

%ifarch %{ix86}
%{__tar} --strip-components=1 -zxf %{SOURCE0}
%endif
%ifarch %{x8664}
%{__tar} --strip-components=1 -zxf %{SOURCE1}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/Zend/lib/Optimizer{,_TS}-%{version},%{_bindir},/etc/php{,4},}

echo "zend_optimizer.version=%{version}" > $RPM_BUILD_ROOT/etc/php4/pack.ini
echo "zend_optimizer.version=%{version}" > $RPM_BUILD_ROOT/etc/php/pack.ini

cd data
install zendid $RPM_BUILD_ROOT%{_bindir}
install poweredbyoptimizer.gif $RPM_BUILD_ROOT%{_sysconfdir}/php
install poweredbyoptimizer.gif $RPM_BUILD_ROOT%{_sysconfdir}/php4
install *.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib

for a in *_comp; do
	d=$(basename $a _comp | tr _ .)
	install -D $a/ZendOptimizer.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer-%{version}/php-$d/ZendOptimizer.so
done
for a in *_comp/TS; do
	d=$(basename $(dirname $a) _comp | tr _ .)
	install -D $a/ZendOptimizer.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer_TS-%{version}/php-$d/ZendOptimizer.so
done

ln -s %{_sysconfdir}/php $RPM_BUILD_ROOT%{_libdir}/Zend/etc
ln -s %{_bindir} $RPM_BUILD_ROOT%{_libdir}/Zend/bin

cat <<'EOF' > zendoptimizer.ini
[Zend]
zend_optimizer.optimization_level=15
zend_extension_manager.optimizer=%{_libdir}/Zend/lib/Optimizer-%{version}
zend_extension_manager.optimizer_ts=%{_libdir}/Zend/lib/Optimizer_TS-%{version}
zend_extension=%{_libdir}/Zend/lib/ZendExtensionManager.so
zend_extension_ts=%{_libdir}/Zend/lib/ZendExtensionManager_TS.so
EOF

install -d $RPM_BUILD_ROOT%{_sysconfdir}/php{,4}/conf.d
install zendoptimizer.ini $RPM_BUILD_ROOT/etc/php4/conf.d/%{name}.ini
install zendoptimizer.ini $RPM_BUILD_ROOT/etc/php/conf.d/%{name}.ini

%clean
rm -rf $RPM_BUILD_ROOT

%preun -n php4-%{name}
if [ "$1" = "0" ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart
fi

%post -n php4-%{name}
[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart

%preun -n php-%{name}
if [ "$1" = "0" ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%post -n php-%{name}
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%post
if [ "$1" = 1 ]; then
%banner -e %{name} <<EOF
Remember to read %{_docdir}/%{name}-%{version}/LICENSE.gz!
EOF
fi

# TODO: trigger for removing [Zend] section from php.ini

%files
%defattr(644,root,root,755)
%doc data/doc LICENSE
%attr(755,root,root) %{_bindir}/zendid
%dir %{_libdir}/Zend
%dir %{_libdir}/Zend/lib
%dir %{_libdir}/Zend/lib/Optimizer-%{version}
%dir %{_libdir}/Zend/lib/Optimizer-%{version}/php-*
%dir %{_libdir}/Zend/lib/Optimizer_TS-%{version}
%dir %{_libdir}/Zend/lib/Optimizer_TS-%{version}/php-*
%attr(755,root,root) %{_libdir}/Zend/lib/Optimizer-%{version}/php-*/ZendOptimizer.so
%attr(755,root,root) %{_libdir}/Zend/lib/Optimizer_TS-%{version}/php-*/ZendOptimizer.so
%attr(755,root,root) %{_libdir}/Zend/lib/ZendExtensionManager.so
%attr(755,root,root) %{_libdir}/Zend/lib/ZendExtensionManager_TS.so
%{_libdir}/Zend/bin
%{_libdir}/Zend/etc

%files -n php4-%{name}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/php4/pack.ini
%config(noreplace) %verify(not md5 mtime size) /etc/php4/conf.d/*.ini
/etc/php4/poweredbyoptimizer.gif

%files -n php-%{name}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/php/pack.ini
%config(noreplace) %verify(not md5 mtime size) /etc/php/conf.d/*.ini
/etc/php/poweredbyoptimizer.gif
