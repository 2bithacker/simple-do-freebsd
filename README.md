Simple DigitalOcean FreeBSD Init
====

By default, (DigitalOcean)[http://digitalocean.com] uses a customized
bsd-cloudinit for initializing FreeBSD droplets from their Metadata API.

This is a simplified version of that, which requires no modification to the
FreeBSD base system and consists of just an rc.d script and a Python script.

h2. Requirements

* python2.7

h2. Usage

Install the `digitalocean` file in /etc/rc.d of a FreeBSD droplet you intend to
use as a snapshot template for new droplets and install `simple-fbsd-init.py` in
`/usr/local/sbin`.

On the next reboot, the script will popular `/etc/rc.conf.d` with `routing`,
`network`, and `hostname` files with the relevant config parameters, and it will
call `resolvconf` with DNS configuration for `vtnet0`.
