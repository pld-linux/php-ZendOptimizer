# DO NOT MODIFY CONTENTS OF PACKAGE - AGAINST LICENSE AND MAKES IT UNDISTRIBUTABLE
# AND ALSO IT IS ALREADY STRIPPED.

%define		no_install_post_strip		1
%define		no_install_post_compress_docs	1
%define		no_install_post_chrpath		1
Summary:	Zend Optimizer - PHP code optimizer
Summary(pl):	Zend Optimizer - optymalizator kodu PHP
Name:		ZendOptimizer
Version:	2.5.10a
Release:	0.9
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
Summary:	php4
Group:		php4
PreReq:		ZendOptimizer = %{version}-%{release}
Requires:	php >= 3:4.0.6
Provides:	ZendOptimizer(php)

%description -n php4-%{name}

%package -n php-%{name}
Summary:	php
Group:		php
PreReq:		ZendOptimizer = %{version}-%{release}
Requires:	php >= 3:5.0.0
Provides:	ZendOptimizer(php)

%description -n php-%{name}

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
install -d $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer-%{version}/php-{4.0.6,4.1.x,4.2.0,4.2.x,4.3.x,4.4.x,5.0.x}
install -d $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer_TS-%{version}/php-{4.2.x,4.3.x,4.4.x,5.0.x}

echo "zend_optimizer.version=%{version}" > $RPM_BUILD_ROOT/etc/php4/pack.ini
echo "zend_optimizer.version=%{version}" > $RPM_BUILD_ROOT/etc/php/pack.ini

cd data
install zendid $RPM_BUILD_ROOT%{_bindir}
install poweredbyoptimizer.gif $RPM_BUILD_ROOT%{_sysconfdir}/php
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
install zendoptimizer.ini $RPM_BUILD_ROOT%{_sysconfdir}/php4/conf.d/%{name}.ini
install zendoptimizer.ini $RPM_BUILD_ROOT%{_sysconfdir}/php/conf.d/%{name}.ini

%clean
rm -rf $RPM_BUILD_ROOT

# NOTE THIS MIGHT BE INSECURE WHEN SOMEONE IS USING COMMERCIAL ZEND PRODUCTS
# THEN AGAIN HE/SHE SHOULD USE THEIR OPTIMIZER
%preun
if [ "$1" = "0" ]; then
	umask 022
	# just php5, php4 has confdir
	for php in /etc/php/php.ini; do
		if [ -f $php ]; then
			echo "deactivating module 'ZendOptimizer.so' in $php" 1>&2
			grep -v '\[Zend\]' $php |\
			grep -v zend_extension |grep -v zend_optimizer > $php.tmp
			mv $php.tmp $php
		fi
	done
	# apache1
	if [ -f /etc/apache/conf.d/??_mod_php4.conf ] && [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
	# apache2
	if [ -f /etc/httpd/httpd.conf/??_mod_php4.conf ] && [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%post
umask 022
for php in /etc/php/php.ini; do
	# just php5, php4 has confdir
	if [ -f $php ]; then
		echo "activating module 'ZendOptimizer.so' in $php" 1>&2
		if grep -q ^zend_optimizer.optimization_level ; then
			optlevel=`grep ^zend_optimizer $php|cut -d'=' -f2|tr -d ' '|tr -d '"'|tr -d "'"|tr -d ';'`
		else
			optlevel="15"
		fi
		cp $php{,.zend-backup}
		grep -v zend_optimizer.optimization_level $php | \
		grep -v zend_extension > $php.tmp
		echo '[Zend]' >> $php.tmp
		echo "zend_optimizer.optimization_level=$optlevel" >> $php.tmp
		echo "zend_extension_manager.optimizer=%{_libdir}/Zend/lib/Optimizer-%{version}" >> $php.tmp
		echo "zend_extension_manager.optimizer_ts=%{_libdir}/Zend/lib/Optimizer_TS-%{version}" >> $php.tmp
		echo "zend_extension=%{_libdir}/Zend/lib/ZendExtensionManager.so" >> $php.tmp
		echo "zend_extension_ts=%{_libdir}/Zend/lib/ZendExtensionManager_TS.so" >> $php.tmp
		mv $php{.tmp,}
	fi
done

# apache1
if [ -f /etc/apache/conf.d/??_mod_php4.conf ] && [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi
# apache2
if [ -f /etc/httpd/httpd.conf/??_mod_php4.conf ] && [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

echo "Remember: Read the %{_docdir}/ZendOptimizer-%{version}/LICENSE.gz !"

# TODO: trigger for removing [Zend] section from php.ini

%files
%defattr(644,root,root,755)
%doc data/doc LICENSE
%attr(755,root,root) %{_bindir}/zendid
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/php/pack.ini
%{_sysconfdir}/php/poweredbyoptimizer.gif

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
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/php4/conf.d/*.ini

%files -n php-%{name}
%defattr(644,root,root,755)
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/php/conf.d/*.ini
