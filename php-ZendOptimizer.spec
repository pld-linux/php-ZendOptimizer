%define _srcname ZendOptimizer-Beta4-Linux-glibc2.1
Summary:	Zend Optimizer - php4 code optimizer
Summary(pl):	Zend Optimizer - optymalizator kodu php4
Name:		ZendOptimizer
Version:	0.98beta4
Release:	1
Group:		Libraries
Group(pl):	Biblioteki
Copyright:	Trial
Source0:	%{_srcname}.tar.gz
URL:		http://www.zend.com/zend/optimizer.php
Requires:	php >= 4.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zend Optimizer - php4 code optimizer

%description -l pl
Zend Optimizer - optymalizator kodu php4

%prep
%setup -q -n %{_srcname}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_libdir}/apache/php/
install ZendOptimizer.so $RPM_BUILD_ROOT/%{_libdir}/apache/php/

gzip -9nf FAQ.txt LICENSE

%preun
if [ -f /etc/httpd/php.ini ]; then
        echo "deactivating module 'ZendOptimizer.so' in php.ini" 1>&2
   perl -pi -e 's|^zend_optimizer.optimization_level|;zend_optimizer.optimization_level|g' \
   /etc/httpd/php.ini
   perl -pi -e 's|^zend_extension=/usr/lib/apache/php/ZendOptimizer.so"|;zend_extension="/usr/lib/apache/php/ZendOptimizer.so"|g' \
   /etc/httpd/php.ini

fi

%post
if [ -f /etc/httpd/php.ini ]; then
        echo "activating module 'ZendOptimizer.so' in php.ini" 1>&2
   perl -pi -e 's|^;zend_optimizer.optimization_level|zend_optimizer.optimization_level|g' \
   /etc/httpd/php.ini
   perl -pi -e 's|^;zend_extension="/usr/lib/apache/php/ZendOptimizer.so"|zend_extension="/usr/lib/apache/php/ZendOptimizer.so"|g' \
   /etc/httpd/php.ini
fi
if [ -f /var/lock/subsys/httpd ]; then
        /etc/rc.d/init.d/httpd restart 1>&2
fi
echo "Remember:Read the /usr/share/doc/ZendOptimizer-%{version}/LICENSE.gz!"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {FAQ.txt,LICENSE}.gz
%doc acceleratedbyoptimizer.gif
%{_libdir}/apache/php/ZendOptimizer.so
