#!/usr/bin/env bash

shopt -s nullglob

yum install -y http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
yum install -y rpmdevtools rpmlint mock
usermod -a -G mock vagrant

mkdir -p /home/vagrant/logstash
cp -R /vagrant/* /home/vagrant/logstash
chown -R vagrant:vagrant /home/vagrant/logstash

### sanity checking package installation (issue #15)
declare -a packages=(epel-release rpmdevtools rpmlint mock)
declare -a missing=()
for i in "${packages[@]}"; do
    rpm -qa | grep -q $i
    if [ $? -ne 0 ]; then
        missing=("${missing[@]}" $i)
    fi
done

if [ ${#missing[@]} -ne 0 ]; then
    echo "The following packages did not install: ${missing[@]}" 1>&2;
fi
