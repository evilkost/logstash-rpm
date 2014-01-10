#!/usr/bin/env sh

VERSION="1.3.2-1"

rpmlint SPECS/logstash.spec
spectool -C SOURCES -g SPECS/logstash.spec
rpmbuild --define "_topdir `pwd`" -bs SPECS/logstash.spec
rpmlint SRPMS/logstash-${VERSION}.el6.src.rpm
mock --resultdir RPMS SRPMS/logstash-${VERSION}.el6.src.rpm
rpmlint RPMS/logstash-${VERSION}.el6.noarch.rpm
