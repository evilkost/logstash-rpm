# Well, logstash (at least at verstion 1.4.2) has some hardcoded [relative] paths (
# So most of installed files will reside in /usr/lib/logstash/{lib, locales, patterns, vendor}
# ... even run script can't be copied to /usr/bin  (

# %define _unpackaged_files_terminate_build 0


#%global bindir %{_bindir}
#%global confdir %{_sysconfdir}/%{name}
%global homedir %{_sharedstatedir}/%{name}
#%global jarpath %{_javadir}
#%global lockfile %{_localstatedir}/lock/subsys/%{name}
%global logdir %{_localstatedir}/log/%{name}
%global piddir %{_localstatedir}/run/%{name}
%global plugindir %{_datadir}/%{name}
#%global sysconfigdir %{_sysconfdir}/sysconfig

%global LS_home %{_libdir}/%{name}

Name:           logstash
Version:        1.4.2
Release:        3%{?dist}
Summary:        A tool for managing events and logs

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://logstash.net
Source0:        https://download.elasticsearch.org/logstash/logstash/%{name}-%{version}.tar.gz
Source1:        logstash.wrapper
Source2:        logstash.logrotate
Source3:        logstash.init
Source4:        logstash.env
Source5:        logstash.service
# BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# due to vendor/bundle
AutoReqProv: no

BuildRequires: systemd

Requires: systemd
Requires: java-1.8.0-openjdk
Requires: jpackage-utils
# Requires:       jruby # maybe later shift to version provided by distribution

# Requires(post): chkconfig initscripts
# Requires(pre):  chkconfig initscripts
# Requires(pre):  shadow-utils

%description
A tool for managing events and logs.

%prep
%setup -q

%build

%install

# Environment file
install -d %{buildroot}%{_sysconfdir}/logstash
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/%{name}.env

%{__sed} -i \
  -e "s|@@@NAME@@@|%{name}|g" \
  -e "s|@@@CONFDIR@@@|%{_sysconfdir}/%{name}|g" \
  -e "s|@@@LOGDIR@@@|%{logdir}|g" \
  -e "s|@@@PLUGINDIR@@@|%{plugindir}|g" \
  -e "s|@@@JAVA_IO_TMPDIR@@@|%{piddir}/java_io|g" \
  %{buildroot}%{_sysconfdir}/%{name}.env


# Systemd unit
install -d %{buildroot}/%{_unitdir}
install -m 755 %{SOURCE5} %{buildroot}/%{_unitdir}/

%{__sed} -i \
  -e "s|@@@LS_HOME@@@|%{LS_home}|g" \
  -e "s|@@@CONFDIR@@@|%{_sysconfdir}/%{name}.d|g" \
  -e "s|@@@USRSHARE@@@|%{_datarootdir}|g" \
  -e "s|@@@ENVFILE@@@|%{_sysconfdir}/%{name}.env|g" \
  %{buildroot}/%{_unitdir}/logstash.service

# Config dir
install -d %{buildroot}%{_sysconfdir}/%{name}.d

# Plugin dir
install -d  %{buildroot}%{plugindir}/inputs
install -d  %{buildroot}%{plugindir}/filters
install -d  %{buildroot}%{plugindir}/outputs
install -d  %{buildroot}%{plugindir}/patterns  # see if it really usable


# Logs
install -d  %{buildroot}%{_localstatedir}/log/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Misc
install -d %{buildroot}%{piddir}
install -d %{buildroot}%{piddir}/java_io


# Executables
# See header, we cannot place executables into the correct place
#  In fact thist script can be replaced with custom, but it doesn't solve other
#  path inconsistencies (.
#
# install -d %{buildroot}%{_bindir}
# install -m 755 bin/logstash %{buildroot}%{_bindir}/logstash
# install -m 755 bin/logstash.lib.sh %{buildroot}%{_bindir}/logstash.lib.sh

# Libs (and almost anything to run daemon)

install -d %{buildroot}%{LS_home}/lib
install -d %{buildroot}%{LS_home}/patterns
install -d %{buildroot}%{LS_home}/locales
install -d %{buildroot}%{LS_home}/vendor
install -d %{buildroot}%{LS_home}/bin

cp -ar patterns/*  %{buildroot}%{LS_home}/patterns/
cp -ar lib/*  %{buildroot}%{LS_home}/lib/
cp -ar locales/*  %{buildroot}%{LS_home}/locales/
cp -ar vendor/*  %{buildroot}%{LS_home}/vendor/
cp -ar bin/*  %{buildroot}%{LS_home}/bin/

# Create Home directory
#   See https://github.com/lfrancke/logstash-rpm/issues/5
install -d  %{buildroot}%{homedir}

%pre
# create logstash group
if ! getent group logstash >/dev/null; then
  groupadd -r logstash
fi

# create logstash user
if ! getent passwd logstash >/dev/null; then
  useradd -r -g logstash -d %{homedir} -s /sbin/nologin -c "Logstash service user" logstash
fi

%post
# read new unit
systemctl daemon-reload

%preun

%clean
# rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
# Systemd service
%{_unitdir}/*

# Executables
# %{_bindir}/*

# Libs
%dir %{LS_home}
%{LS_home}/*

# Config
%{_sysconfdir}/%{name}.env
%dir  %{_sysconfdir}/%{name}.d/


# Plugin dir
%dir %{plugindir}/inputs
%dir %{plugindir}/filters
%dir %{plugindir}/outputs
%dir %{plugindir}/patterns

# Logrotate
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%defattr(-,%{name},%{name},-)
%dir %{logdir}/
%dir %{piddir}/

# Home directory
%dir %{homedir}/

%changelog
* Tue Mar 31 2015 vgologuz@redhat.com 1.4.2-3
- Updated logstash.service: log file should be inside /var/log/logstash/ dir

* Wed Mar 18 2015 vgologuz@redhat.com 1.4.2-2
- Requiring java 1.8, since 1.7 not available at Fedora 21

* Wed Jan 28 2015 vgologuz@redhat.com 1.4.2-1
- Updated to new upstream distribution format. Replaced sysv init script with
  systemd unit. Current RPM target: Fedora 20+.

* Mon Jan 26 2015 BogusDateBot
- Eliminated rpmbuild "bogus date" warnings due to inconsistent weekday,
  by assuming the date is correct and changing the weekday.
  Tue Jan 11 2013 --> Tue Jan 08 2013 or Fri Jan 11 2013 or Tue Jan 15 2013 or ....
  Mon Feb 06 2014 --> Mon Feb 03 2014 or Thu Feb 06 2014 or Mon Feb 10 2014 or ....

* Thu Feb 06 2014 lars.francke@gmail.com 1.3.3-2
- Start script now allows multiple server types (web & agent) at the same time (Thanks to Brad Quellhorst)
- Logging can be configured via LOGSTASH_LOGLEVEL flag in /etc/sysconfig/logstash
- Default log level changed from INFO TO WARN

* Mon Jan 20 2014 dmaher@mozilla.com 1.3.3-1
- Update logstash to version 1.3.3

* Fri Jan 10 2014 lars.francke@gmail.com 1.3.2-1
- Update logstash to version 1.3.2 (Thanks to Brad Quellhorst)

* Thu Dec 12 2013 lars.francke@gmail.com 1.3.1-1
- Update logstash to version 1.3.1
- Fixed Java version to 1.7 as 1.5 does not work

* Wed Dec 11 2013 lars.francke@gmail.com 1.2.2-2
- Fixed reference to removed jre7 package
- Fixed rpmlint warning about empty dummy.rb file
- Fixes stderr output not being captured in logfile
- Fixed home directory location (now in /var/lib/logstash)

* Mon Oct 28 2013 lars.francke@gmail.com 1.2.2-1
- Update logstash version to 1.2.2
- Change default log level from WARN to INFO

* Wed Jun 12 2013 lars.francke@gmail.com 1.1.13-1
- Update logstash version to 1.1.13

* Thu May 09 2013 dmaher@mozilla.com 1.1.12-1
- Update logstash version to 1.1.12

* Thu Apr 25 2013 dmaher@mozilla.com 1.1.10-1
- Use flatjar instead of monolithic
- Update logstash version to 1.1.10

* Tue Jan 22 2013 dmaher@mozilla.com 1.1.9-1
- Add chkconfig block to init
- Update logstash version to 1.1.9

* Fri Jan 11 2013 lars.francke@gmail.com 1.1.5-1
- Initial version
