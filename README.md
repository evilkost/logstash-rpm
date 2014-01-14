RPM Specs for Logstash
======================

Tries to follow the [Java packaging guidelines](https://fedoraproject.org/wiki/Packaging:Java) from Fedora.

* Jar: `/usr/share/java/logstash.jar`
* Config: `/etc/logstash/`
* Plugins: `/usr/share/logstash/`
* Script: `/usr/bin/logstash`
* Sysconfig: `/etc/sysconfig/logstash`
* logrotate: `/etc/logrotate.d/logstash`
* Logs: `/var/log/logstash/logstash.log`
* PID file: `/var/run/logstash/logstash.pid`
* init script: `/etc/rc.d/init.d/logstash`
* Running as user `logstash` in group `logstash` with home directory `/var/lib/logstash`

Vagrant
-------

There is a simple [Vagrantfile](http://www.vagrantup.com/) that prepares a CentOS VM with all the necessary packages to build RPMs. This is useful if you're on a machine that doesn't have those tools pre-installed:

    vagrant up

When you log in you'll have a `logstash` directory which contains a `makerpm.sh` file which - when executed - should run through all the steps to build a final RPM which will end up in the `RPMS` directory.

Acknowledgments
---------------

Inspiration for this came from various other projects:
* https://github.com/NumberFour/logstash-rpms
* https://github.com/mhorbul/logstash-rpm
* https://github.com/piojo/logstash-rpm
