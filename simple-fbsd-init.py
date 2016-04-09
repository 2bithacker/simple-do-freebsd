#!/usr/bin/env python2.7

import urllib2
import json
import os

METADATA_IP = '169.254.169.254'
BASE = ''
RESOLVCONF = '/sbin/resolvconf -a vtnet0'


def fetch_hostdata(metadata_ip):
    metadata = urllib2.urlopen('http://'+metadata_ip+'/metadata/v1.json')
    data = json.load(metadata)
    return data


def write_network(metadata):
    fh = open(BASE+'/etc/rc.conf.d/network', 'w+')
    fh.write("# simple-fbsd-init network configuration\n")

    if 'public' in metadata['interfaces']:
        public = metadata['interfaces']['public'][0]
        if 'ipv4' in public:
            c = 'ifconfig_vtnet0="inet {0[ip_address]} netmask {0[netmask]}"'
            fh.write(c.format(public['ipv4'])+"\n")
        if 'ipv6' in public:
            c = 'ifconfig_vtnet0_ipv6="inet6 {0[ip_address]}/{0[cidr]}"'
            fh.write(c.format(public['ipv6'])+"\n")
    if 'private' in metadata['interfaces']:
        private = metadata['interfaces']['private'][0]
        if 'ipv4' in private:
            c = 'ifconfig_vtnet1="inet {0[ip_address]} netmask {0[netmask]}"'
            fh.write(c.format(private['ipv4'])+"\n")

    fh.close()


def write_hostname(metadata):
    fh = open(BASE+'/etc/rc.conf.d/hostname', 'w+')
    fh.write("# simple-fbsd-init hostname configuration\n")
    c = 'hostname="{0[hostname]}"'
    fh.write(c.format(metadata)+"\n")
    fh.close()


def write_routing(metadata):
    fh = open(BASE+'/etc/rc.conf.d/routing', 'w+')
    fh.write("# simple-fbsd-init routing configuration\n")

    if 'ipv4' in metadata['interfaces']['public'][0]:
        c = 'defaultrouter="{0[gateway]}"'
        fh.write(c.format(metadata['interfaces']['public'][0]['ipv4'])+"\n")
    if 'ipv6' in metadata['interfaces']['public'][0]:
        c = 'ipv6_defaultrouter="{0[gateway]}"'
        fh.write(c.format(metadata['interfaces']['public'][0]['ipv6'])+"\n")


def update_resolvconf(metadata):
    rc = os.popen(RESOLVCONF, 'w')
    for ns in metadata['dns']['nameservers']:
        rc.write("nameserver {0}\n".format(ns))
    rc.close()


def write_configuration(metadata):
    write_network(metadata)
    write_hostname(metadata)
    write_routing(metadata)
    update_resolvconf(metadata)

if __name__ == '__main__':
    hostdata = fetch_hostdata(METADATA_IP)
    write_configuration(hostdata)
