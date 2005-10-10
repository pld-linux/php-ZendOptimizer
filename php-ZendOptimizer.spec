# DO NOT MODIFY CONTENTS OF PACKAGE - AGAINST LICENSE AND MAKES IT UNDISTRIBUTABLE
# AND ALSO IT IS ALREADY STRIPPED.

%define		no_install_post_strip		1
%define		no_install_post_compress_docs	1
%define		no_install_post_chrpath		1
Summary:	Zend Optimizer - PHP code optimizer
Summary(pl):	Zend Optimizer - optymalizator kodu PHP
Name:		ZendOptimizer
Version:	2.5.10a
Release:	0.30
License:	Zend License, distributable only if unmodified and for free (see LICENSE)
Group:		Libraries
Source0:	http://downloads.zend.com/optimizer/2.5.10/%{name}-%{version}-linux-glibc21-i386.tar.gz
# Source0-md5:	3064cb6d33f0d4800cf84b8a5521cd48
Source1:	http://downloads.zend.com/optimizer/2.5.10/%{name}-%{version}-linux-glibc23-x86_64.tar.gz
# Source1-md5:	6d7e50b1875fb77eff7d0cc6ff45db32
URL:		http://www.zend.com/zend/optimizer.php
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	tar >= 1:1.15.1
# circular dependency, so ones upgraded are forced to choose php and
# ones that want to install specific for specific version need not to
# install ZendOptimizer separately
Requires:	%{name}(php) = %{version}-%{release}
Requires(triggerpostun):	sed >= 4.0
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zend Optimizer - PHP code optimizer.

%description -l pl
Zend Optimizer - optymalizator kodu PHP.

%package -n php4-%{name}
Summary:	Zend Optimizer for PHP 4.x
Summary(pl):	Zend Optimizer dla PHP 4.x
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	php4-common >= 3:4.0.6
Provides:	%{name}(php) = %{version}-%{release}

%description -n php4-%{name}
Zend Optimizer for PHP 4.x.

%description -n php4-%{name} -l pl
Zend Optimizer dla PHP 4.x.

%package -n php-%{name}
Summary:	Zend Optimizer for PHP 5.x
Summary(pl):	Zend Optimizer dla PHP 5.x
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	php-common >= 4:5.0.0
Provides:	%{name}(php) = %{version}-%{release}

%description -n php-%{name}
Zend Optimizer for PHP 5.x.

%description -n php-%{name} -l pl
Zend Optimizer dla PHP 5.x.

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
install -d $RPM_BUILD_ROOT{%{_bindir},/etc/php4,/etc/php}

cd data
for a in *_comp; do
	d=$(basename $a _comp | tr _ .)
	install -D $a/ZendOptimizer.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer-%{version}/php-$d/ZendOptimizer.so
done
for a in *_comp/TS; do
	d=$(basename $(dirname $a) _comp | tr _ .)
	install -D $a/ZendOptimizer.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer_TS-%{version}/php-$d/ZendOptimizer.so
done

install zendid $RPM_BUILD_ROOT%{_bindir}
install poweredbyoptimizer.gif $RPM_BUILD_ROOT%{_sysconfdir}/php
install poweredbyoptimizer.gif $RPM_BUILD_ROOT%{_sysconfdir}/php4
install *.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib
ln -s %{_sysconfdir}/php $RPM_BUILD_ROOT%{_libdir}/Zend/etc
ln -s %{_bindir} $RPM_BUILD_ROOT%{_libdir}/Zend/bin

cat <<'EOF' > zendoptimizer.ini
; ZendOptimizer user settings.
[Zend]
zend_optimizer.optimization_level=15
EOF

cat <<'EOF' > pack.ini
; ZendOptimizer package settings. Overwritten with each upgrade.
; if you need to add options, edit %{name}.ini instead
[Zend]
zend_optimizer.version=%{version}
zend_extension_manager.optimizer=%{_libdir}/Zend/lib/Optimizer-%{version}
zend_extension_manager.optimizer_ts=%{_libdir}/Zend/lib/Optimizer_TS-%{version}
zend_extension=%{_libdir}/Zend/lib/ZendExtensionManager.so
zend_extension_ts=%{_libdir}/Zend/lib/ZendExtensionManager_TS.so
EOF

install -d $RPM_BUILD_ROOT%{_sysconfdir}/php{,4}/conf.d
install zendoptimizer.ini $RPM_BUILD_ROOT/etc/php4/conf.d/%{name}.ini
install zendoptimizer.ini $RPM_BUILD_ROOT/etc/php/conf.d/%{name}.ini
install pack.ini $RPM_BUILD_ROOT/etc/php4/conf.d/%{name}_pack.ini
install pack.ini $RPM_BUILD_ROOT/etc/php/conf.d/%{name}_pack.ini

%clean
rm -rf $RPM_BUILD_ROOT

%preun -n php4-%{name}
if [ "$1" = "0" ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart
fi

%post -n php4-%{name}
# let /usr/lib/Zend/etc point to php's config dir. php which installed first wins.
# not sure how critical is existence of this etc link at all.
if [ ! -L %{_libdir}/Zend/etc ]; then
	ln -snf /etc/php4 %{_libdir}/Zend/etc
fi
[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart


%preun -n php-%{name}
if [ "$1" = "0" ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%post -n php-%{name}
# let /usr/lib/Zend/etc point to php's config dir. php which installed first wins.
# not sure how critical is existence of this etc link at all.
if [ ! -L %{_libdir}/Zend/etc ]; then
	ln -snf /etc/php %{_libdir}/Zend/etc
fi
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%post
if [ "$1" = 1 ]; then
%banner -e %{name} <<EOF
Remember to read %{_docdir}/%{name}-%{version}/LICENSE.gz!
EOF
fi

%triggerpostun -n php4-%{name} -- %{name} < 2.5.10a-0.20
if [ -f /etc/php4/php.ini ]; then
	cp -f /etc/php4/conf.d/ZendOptimizer.ini{,.rpmnew}
	sed -ne '/^\(zend_\|\[Zend\]\)/{/^zend_extension\(_manager\.optimizer\)\?\(_ts\)\?=/d;p}' /etc/php4/php.ini > /etc/php4/conf.d/ZendOptimizer.ini
	cp -f /etc/php4/php.ini{,.rpmsave}
	sed -i -e '/^\(zend_\|\[Zend\]\)/d' /etc/php4/php.ini
fi

%triggerpostun -- %{name} < 2.5.10a-0.20
if [ -f /etc/php/php.ini ]; then
	cp -f /etc/php/conf.d/ZendOptimizer.ini{,.rpmnew}
	sed -ne '/^\(zend_\|\[Zend\]\)/{/^zend_extension\(_manager\.optimizer\)\?\(_ts\)\?=/d;p}' /etc/php/php.ini > /etc/php/conf.d/ZendOptimizer.ini
	cp -f /etc/php/php.ini{,.rpmsave}
	sed -i -e '/^\(zend_\|\[Zend\]\)/d' /etc/php/php.ini
fi

%files
%defattr(644,root,root,755)
%doc data/doc/* LICENSE
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
%ghost %{_libdir}/Zend/etc

%files -n php4-%{name}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/php4/conf.d/%{name}.ini
%config %verify(not md5 mtime size) /etc/php4/conf.d/%{name}_pack.ini
/etc/php4/poweredbyoptimizer.gif

%files -n php-%{name}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/php/conf.d/%{name}.ini
%config %verify(not md5 mtime size) /etc/php/conf.d/%{name}_pack.ini
/etc/php/poweredbyoptimizer.gif
