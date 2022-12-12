%global __os_install_post %{nil}
%define __strip /bin/true
%define __ldd /bin/true
%global _enable_debug_package 0
%global debug_package %{nil}

Name:           kyocera-sane-re
Version:        1.1
Release:        alt2
BuildArch:		x86_64
Summary:        Kyocera SANE package for Kyocera (repack original)
Packager:       w00zy <w00zy@yandex.ru>
License:        GPL+
URL:            https://www.kyoceradocumentsolutions.ru/ru.html
Group:          System/Configuration/Printing
Obsoletes:      kyocera-sane
Provides:		kyocera-sane
Requires:       libsane sane
Requires:		glibc >= 2.2.5
AutoReqProv:    no
###BuildRequires: rpm-utils
Source0:        kyocera-sane-1.1-0228.x86_64.rpm

##%%ifarch x86_64

##%%endif
##%%ifarch i386
##Source0:        kyocera-sane-1.1-0228.x86_64.rpm
##%%endif

Source1: 90-kyocera-permissions.rules

##Patch:        permissions.rules.path

%description
 * Kyocera MFP supported device:
    * FS-1020 MFP usb 0x0482 0x0495
    * FS-1120 MFP usb 0x0482 0x0496
    * FS-1025 MFP usb 0x0482 0x0497
    * FS-1125 MFP usb 0x0482 0x0498
    * FS-1220 MFP usb 0x0482 0x04FD
    * FS-1320 MFP usb 0x0482 0x04FE
    * FS-1325 MFP usb 0x0482 0x04FF

%post
sed -i '/kyocera/d' /etc/sane.d/dll.conf
echo kyocera >> /etc/sane.d/dll.conf
sed -i '/kyocera_gdi_a3/d' /etc/sane.d/dll.conf
echo kyocera_gdi_a3 >> /etc/sane.d/dll.conf
%{__ln_s} -f %{_libdir}/libkmip.so.1.0.705 %{_libdir}/libkmip.so.1
#ln -s /usr/lib64/libkmip.so.1.0.705 /usr/lib64/libkmip.so.1
%{__ln_s} -f %{_libdir}/sane/libsane-kyocera.so.1.0.24 %{_libdir}/sane/libsane-kyocera.so.1
#ln -s /usr/lib64/sane/libsane-kyocera.so.1.0.24  /usr/lib64/sane/libsane-kyocera.so.1
%{__ln_s} -f %{_libdir}/sane/libsane-kyocera_gdi_a3.so.1.0.25 %{_libdir}/sane/libsane-kyocera_gdi_a3.so.1
#ln -s /usr/lib64/sane/libsane-kyocera_gdi_a3.so.1.0.25  /usr/lib64/sane/libsane-kyocera_gdi_a3.so.1
ldconfig

%postun
if [ $1 -eq 0 ] ; then
	if [ -d /usr/local/kyocera ]; then
		rm -rf /usr/local/kyocera
	fi
fi
if [ ! -e /usr/lib64/libkmip.so.1.0.705 ]; then
      rm /usr/lib64/libkmip.so.1
fi
if [ ! -e /usr/lib64/sane/libsane-kyocera.so.1.0.24 ]; then
      rm /usr/lib64/sane/libsane-kyocera.so.1
fi
if [ ! -e /usr/lib64/sane/libsane-kyocera_gdi_a3.so.1.0.25 ]; then
      rm /usr/lib64/sane/libsane-kyocera_gdi_a3.so.1
fi
ldconfig

%pre
if [ -e /usr/lib64/libkmip.so.1 ]; then
    rm /usr/lib64/libkmip.so.1
fi
if [ -e /usr/lib64/sane/libsane-kyocera.so.1 ]; then
    rm /usr/lib64/sane/libsane-kyocera.so.1
fi
if [ -e /usr/lib64/sane/libsane-kyocera_gdi_a3.so.1 ]; then
    rm /usr/lib64/sane/libsane-kyocera_gdi_a3.so.1
fi

%prep
%set_verify_elf_method skip

if [ -d %{_builddir}/%{name}-%{version} ]; then
    %{__rm} -fr %{_builddir}/%{name}-%{version}/*
fi

%{__mkdir} -p %{name}-%{version}
cd %{name}-%{version}

rpm2cpio %{SOURCE0} | %{__cpio} -idmv
### %patch -p0

%build
%clean_buildroot

%install
export DONT_STRIP=1

%{__install} -d -m 755 %{buildroot}/etc/udev/rules.d
%{__install} -d -m 755 %{buildroot}/usr/local/kyocera/scanner
%{__cp} -fr %SOURCE1 %{buildroot}/etc/udev/rules.d
%{__cp} -fr %{_builddir}/%{name}-%{version}/etc %{buildroot}
%{__cp} -fr %{_builddir}/%{name}-%{version}/usr %{buildroot}

%{__rm} -fr %{_builddir}/%{name}-%{version}/*

%files
%defattr(-,root,root)
%attr(644, root, root) %config %{_sysconfdir}/udev/rules.d/90-kyocera-permissions.rules
%attr(644, root, root) %config %{_sysconfdir}/sane.d/kyocera.conf
%attr(644, root, root) %config %{_sysconfdir}/sane.d/kyocera_gdi_a3.conf
%dir %attr(1777, root, root) %{_prefix}/local/kyocera
%dir %attr(1777, root, root) %{_prefix}/local/kyocera/scanner

%{_libdir}/libkmip.so.1.0.705
%{_libdir}/sane/libsane-kyocera.la
%{_libdir}/sane/libsane-kyocera.so.1.0.24
%{_libdir}/sane/libsane-kyocera_gdi_a3.la
%{_libdir}/sane/libsane-kyocera_gdi_a3.so.1.0.25

%changelog
* Wed Jul 25 2022 w00zy <w00zy@yandex.ru>
- Repack for distribution Alt Linux P10

* Mon Feb 17 2014 Ariel Edera <ArielRamonito.Edera@ddp.kyocera.com> 1.1.0217
- First build
