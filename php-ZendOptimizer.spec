# DO NOT MODIFY CONTENTS OF PACKAFE - AGAINST LICENSE AND MAKES IT UNDISTRIBUTABLE
# AND ALSO IT IS ALREADY STRIPPED.

%define		no_install_post_strip		1
%define		no_install_post_compress_docs	1
%define		no_install_post_chrpath		1
Summary:	Zend Optimizer - PHP4 code optimizer
Summary(pl):	Zend Optimizer - optymalizator kodu PHP4
Name:		ZendOptimizer
Version:	2.5.3
Release:	1
License:	Zend License, distributable only if unmodified and for free (see LICENSE)
Group:		Libraries
Source0:	%{name}-%{version}-linux-glibc21-i386.tar.gz
# Source0-md5:	dae8497abc6b5596dc29c265d0978d79
Source1:	%{name}-%{version}-linux-glibc23-amd64.tar.gz
# Source1-md5:	007b4e3d7911ff03b760ec773472a2bb
URL:		http://www.zend.com/zend/optimizer.php
Requires(post):	grep >= 2:2.5.1
Requires(post):	sed >= 4.0.0
Requires(post):	/usr/bin/perl
# php4 provides php with epoch 0 while php provides php with epoch 3, workaround
Requires:	php >= 0:4.0.6
ExclusiveArch:	%{ix86} amd64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zend Optimizer - PHP code optimizer.

%description -l pl
Zend Optimizer - optymalizator kodu PHP.

%prep
%setup -q -c

%ifarch %{ix86}
%{__tar} xfz %{SOURCE0}
%endif
%ifarch amd64
%{__tar} xfz %{SOURCE1}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/Zend/lib/Optimizer{,_TS}-%{version},%{_bindir},/etc/php,}
install -d  $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer-%{version}/php-{4.0.6,4.1.x,4.2.0,4.2.x,4.3.x,5.0.0}
install -d $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer_TS-%{version}/php-{4.2.x,4.3.x,5.0.0}

%ifarch %{ix86}
cd %{name}-%{version}-linux-glibc21-i386
%endif

%ifarch amd64
cd  %{name}-%{version}-linux-glibc23-amd64
%endif

echo "zend_optimizer.version=%{version}" > $RPM_BUILD_ROOT%{_sysconfdir}/php/pack.ini

cd data
install zendid $RPM_BUILD_ROOT%{_bindir}
install poweredbyoptimizer.gif $RPM_BUILD_ROOT%{_sysconfdir}/php
install *.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib

install 4_0_6_comp/ZendOptimizer.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer-%{version}/php-4.0.6
install 4_1_x_comp/ZendOptimizer.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer-%{version}/php-4.1.x
install 4_2_0_comp/ZendOptimizer.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer-%{version}/php-4.2.0
install 4_2_x_comp/ZendOptimizer.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer-%{version}/php-4.2.x
install 4_3_x_comp/ZendOptimizer.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer-%{version}/php-4.3.x
install 5_0_0_comp/ZendOptimizer.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer-%{version}/php-5.0.0

install 4_2_x_comp/TS/ZendOptimizer.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer_TS-%{version}/php-4.2.x
install 4_3_x_comp/TS/ZendOptimizer.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer_TS-%{version}/php-4.3.x
install 5_0_0_comp/TS/ZendOptimizer.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Optimizer_TS-%{version}/php-5.0.0

ln -s /etc/php  $RPM_BUILD_ROOT%{_libdir}/Zend/etc
ln -s %{_bindir} $RPM_BUILD_ROOT%{_libdir}/Zend//bin

%clean
rm -rf $RPM_BUILD_ROOT

# NOTE THIS MIGHT BE INSECURE WHEN SOMEONE IS USING COMMERCIAL ZEND PRODUCTS
# THEN AGAIN HE/SHE SHOULD USE THEIR OPTIMIZER

%preun
if [ -f /etc/php/php.ini ]; then
        echo "deactivating module 'ZendOptimizer.so' in php.ini" 1>&2
#perl -pi -e 's|^zend_optimizer.optimization_level|;zend_optimizer.optimization_level|g' \
#	/etc/php/php.ini
	grep -v '\[Zend\]' /etc/php/php.ini |\
	grep -v zend_extension |grep -v zend_optimizer > /etc/php/php.ini.tmp
	mv /etc/php/php.ini.tmp /etc/php/php.ini
fi
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%post
if [ -f /etc/php/php.ini ]; then
	echo "activating module 'ZendOptimizer.so' in php.ini" 1>&2
	if grep -q ^zend_optimizer.optimization_level  ; then
	optlevel=`grep ^zend_optimizer /etc/php/php.ini|cut -d'=' -f2|tr -d ' '|tr -d '"'|tr -d "'"|tr -d ';'`
	else
	optlevel="15"
	fi
	cp /etc/php/php.ini{,.zend-backup}
	grep -v zend_optimizer.optimization_level /etc/php/php.ini | \
	grep -v zend_extension  > /etc/php/php.ini.tmp
	echo '[Zend]' >> /etc/php/php.ini.tmp
	echo "zend_optimizer.optimization_level=$optlevel" >> /etc/php/php.ini.tmp
	echo "zend_extension_manager.optimizer=%{_libdir}/Zend/lib/Optimizer-%{version}"  >> /etc/php/php.ini.tmp
	echo "zend_extension_manager.optimizer_ts=%{_libdir}/Zend/lib/Optimizer_TS-%{version}" >> /etc/php/php.ini.tmp
	echo "zend_extension=%{_libdir}/Zend/lib/ZendExtensionManager.so" >> /etc/php/php.ini.tmp
	echo "zend_extension_ts=%{_libdir}/Zend/lib/ZendExtensionManager_TS.so" >> /etc/php/php.ini.tmp
	mv /etc/php/php.ini{.tmp,}
fi
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

echo "Remember:Read the /usr/share/doc/ZendOptimizer-%{version}/LICENSE!"

%files
%defattr(644,root,root,755)
%ifarch %{ix86}
%doc %{name}-%{version}-linux-glibc21-i386/data/doc %{name}-%{version}-linux-glibc21-i386/LICENSE
%endif
%ifarch amd64
%doc %{name}-%{version}-linux-glibc23-amd64/data/doc %{name}-%{version}-linux-glibc23-amd64/LICENSE
%endif
%attr(755,root,root) %{_bindir}/zendid
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/php/pack.ini
%{_sysconfdir}/php/poweredbyoptimizer.gif
%dir %{_libdir}/Zend
%dir %{_libdir}/Zend/lib/
%dir %{_libdir}/Zend/lib/Optimizer-2.5.3/php-4.0.6
%dir %{_libdir}/Zend/lib/Optimizer-2.5.3/php-4.1.x
%dir %{_libdir}/Zend/lib/Optimizer-2.5.3/php-4.2.0
%dir %{_libdir}/Zend/lib/Optimizer-2.5.3/php-4.2.x
%dir %{_libdir}/Zend/lib/Optimizer-2.5.3/php-4.3.x
%dir %{_libdir}/Zend/lib/Optimizer-2.5.3/php-5.0.0
%dir %{_libdir}/Zend/lib/Optimizer-2.5.3
%dir %{_libdir}/Zend/lib/Optimizer_TS-2.5.3
%dir %{_libdir}/Zend/lib/Optimizer_TS-2.5.3/php-4.2.x
%dir %{_libdir}/Zend/lib/Optimizer_TS-2.5.3/php-4.3.x
%dir %{_libdir}/Zend/lib/Optimizer_TS-2.5.3/php-5.0.0
%{_libdir}/Zend/bin
%{_libdir}/Zend/etc
%{_libdir}/Zend/lib/Optimizer-2.5.3/php-4.0.6/ZendOptimizer.so
%{_libdir}/Zend/lib/Optimizer-2.5.3/php-4.1.x/ZendOptimizer.so
%{_libdir}/Zend/lib/Optimizer-2.5.3/php-4.2.0/ZendOptimizer.so
%{_libdir}/Zend/lib/Optimizer-2.5.3/php-4.2.x/ZendOptimizer.so
%{_libdir}/Zend/lib/Optimizer-2.5.3/php-4.3.x/ZendOptimizer.so
%{_libdir}/Zend/lib/Optimizer-2.5.3/php-5.0.0/ZendOptimizer.so
%{_libdir}/Zend/lib/ZendExtensionManager.so
%{_libdir}/Zend/lib/Optimizer_TS-2.5.3/php-4.2.x/ZendOptimizer.so
%{_libdir}/Zend/lib/Optimizer_TS-2.5.3/php-4.3.x/ZendOptimizer.so
%{_libdir}/Zend/lib/Optimizer_TS-2.5.3/php-5.0.0/ZendOptimizer.so
%{_libdir}/Zend/lib/ZendExtensionManager_TS.so
