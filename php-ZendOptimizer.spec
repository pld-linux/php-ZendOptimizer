Summary:	Zend Optimizer - php code optimizer
Summary(pl):	Zend Optimizer - optymalizator kodu php
Name:		ZendOptimizer
Version:	2.5.3
Release:	1
License:	Trial, not distributable
Group:		Libraries
Source0:	%{name}-%{version}-linux-glibc21-i386.tar.gz
NoSource:	0
URL:		http://www.zend.com/zend/optimizer.php
Requires:	php >= 5.0.0
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zend Optimizer - php code optimizer.

%description -l pl
Zend Optimizer - optymalizator kodu php.

%prep
%setup -q -n %{name}-%{version}-linux-glibc21-i386

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/apache/php

install data/5_0_0_comp/ZendOptimizer.so $RPM_BUILD_ROOT%{_libdir}/apache/php

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ -f /etc/php/php.ini ]; then
	echo "deactivating module 'ZendOptimizer.so' in php.ini" 1>&2
	perl -pi -e 's|^zend_optimizer.optimization_level|;zend_optimizer.optimization_level|g' \
		/etc/php/php.ini
	perl -pi -e 's|^zend_extension=/usr/lib/apache/php/ZendOptimizer.so"|;zend_extension="/usr/lib/apache/php/ZendOptimizer.so"|g' \
		/etc/php/php.ini
fi

%post
if [ -f /etc/php/php.ini ]; then
	echo "activating module 'ZendOptimizer.so' in php.ini" 1>&2
	perl -pi -e 's|^;zend_optimizer.optimization_level|zend_optimizer.optimization_level|g' \
		/etc/php/php.ini
	perl -pi -e 's|^;zend_extension="/usr/lib/apache/php/ZendOptimizer.so"|zend_extension="/usr/lib/apache/php/ZendOptimizer.so"|g' \
		/etc/php/php.ini
fi
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi
echo "Remember:Read the /usr/share/doc/ZendOptimizer-%{version}/LICENSE.gz!"

%files
%defattr(644,root,root,755)
%doc data/doc/* data/poweredbyoptimizer.gif
%attr(755,root,root) %{_libdir}/apache/php/ZendOptimizer.so
