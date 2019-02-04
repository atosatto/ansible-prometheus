"""Prometheus Jinja2 filters"""
import re


PROM_SYSTEM =  {
    'Linux': 'linux',
    'Darwin': 'darwin',
    'FreeBSD': 'freebsd',
    'NetBSD': 'netbsd',
    'OpenBSD': 'openbsd'
}

PROM_ARCHITECTURE = {
    'x86_64': 'amd64',
    'i386': '386',
    'armv6l': 'armv6',
    'armv7l': 'armv7'
}


def prometheus_release_build(hostvars, promrelease):

    architecture = hostvars['ansible_architecture']
    system = hostvars['ansible_system']

    version = promrelease
    if promrelease != 'latest':
        version = re.sub('^v(.*)$', '\\1', promrelease)

    return 'prometheus-' + version + '.' + PROM_SYSTEM[system] + '-' + PROM_ARCHITECTURE[architecture]


class FilterModule(object):


    def filters(self):
        return {
            'prometheus_release_build': prometheus_release_build
        }
