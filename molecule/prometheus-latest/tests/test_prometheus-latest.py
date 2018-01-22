import os
import re
import json
import urllib2

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

prom_last_release = re.sub('^v(.*)$', '\\1',
        json.loads(urllib2.urlopen("https://api.github.com/repos/prometheus/prometheus/releases/latest").read())["tag_name"])
prom_last_artifact = "prometheus-" + prom_last_release + ".linux-amd64"


def test_prometheus_binaries(host):

    promd = host.file('/usr/local/bin/prometheus')
    assert promd.exists
    assert promd.is_symlink
    assert promd.linked_to == '/opt/' + prom_last_artifact + '/prometheus'

    promt = host.file('/usr/local/bin/promtool')
    assert promt.exists
    assert promt.is_symlink
    assert promt.linked_to == '/opt/' + prom_last_artifact + '/promtool'


def test_prometheus_release(host):

    cmd = host.run('/usr/local/bin/prometheus --version')

    assert 'version ' + prom_last_release in cmd.stderr
