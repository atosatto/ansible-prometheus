import os
import re
from github import Github

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

gh = Github(os.getenv('GITHUB_API_TOKEN', None))
prom_release = re.sub('^v(.*)$', '\\1', gh.get_repo('prometheus/prometheus').get_release("v1.8.2").tag_name)
prom_artifact = "prometheus-" + prom_release + ".linux-amd64"


def test_prometheus_binaries(host):

    promd = host.file('/usr/local/bin/prometheus')
    assert promd.exists
    assert promd.is_symlink
    assert promd.linked_to == '/opt/' + prom_artifact + '/prometheus'

    promt = host.file('/usr/local/bin/promtool')
    assert promt.exists
    assert promt.is_symlink
    assert promt.linked_to == '/opt/' + prom_artifact + '/promtool'


def test_prometheus_release(host):

    cmd = host.run('/usr/local/bin/prometheus --version')

    assert 'version ' + prom_release in (cmd.stdout + cmd.stderr)


def validate_prometheus_config(host):

    host.run_test("/usr/local/bin/promtool check-config /etc/prometheus/prometheus.yml")


def validate_prometheus_rules(host):

    host.run_test("/usr/local/bin/promtool check-rules /etc/prometheus/rules/prometheus.yml")
