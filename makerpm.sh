#!/usr/bin/env sh

# ! require mock ~ 1.2+  (dnf, nspawn chroot etc)

VERSION="1.4.2-1"
DIST="fc20"

# rpmlint SPECS/logstash.spec
spectool -C SOURCES -g SPECS/logstash.spec
rpmbuild --define "_topdir `pwd`" -bs SPECS/logstash.spec
# rpmlint SRPMS/logstash-${VERSION}.${DIST}.src.rpm
mock --new-chroot --dnf --no-cleanup-after --no-clean --resultdir RPMS `pwd`/SRPMS/logstash-${VERSION}.${DIST}.src.rpm 

  # --no-cleanup-after --no-clean  
  #  --resultdir RPMS `pwd`/SRPMS/logstash-${VERSION}.${DIST}.src.rpm

  # rpmlint RPMS/logstash-${VERSION}.${DIST}.noarch.rpm
