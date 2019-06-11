import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_prometheus_config(host):

    d = host.file('/etc/prometheus/')
    assert d.exists
    assert d.user == 'prometheus'
    assert d.group == 'prometheus'
    assert oct(d.mode) == '0755'

    f = host.file('/etc/prometheus/prometheus.yml')
    assert f.exists
    assert f.user == 'prometheus'
    assert f.group == 'prometheus'
    assert oct(f.mode) == '0640'

    host.run("/usr/local/bin/promtool check config /etc/prometheus/prometheus.yml").rc == 0


def test_prometheus_rules(host):

    d = host.file('/etc/prometheus/rules')
    assert d.exists
    assert d.user == 'prometheus'
    assert d.group == 'prometheus'
    assert oct(d.mode) == '0755'

    f = host.file('/etc/prometheus/rules/prometheus.yml')
    assert f.exists
    assert f.user == 'prometheus'
    assert f.group == 'prometheus'
    assert oct(f.mode) == '0640'

    host.run("/usr/local/bin/promtool check rules /etc/prometheus/rules/prometheus.yml").rc == 0


def test_prometheus_tsdb(host):

    d = host.file('/var/lib/prometheus/')
    assert d.exists
    assert d.user == 'prometheus'
    assert d.group == 'prometheus'
    assert oct(d.mode) == '0755'


def test_prometheus_service(host):

    s = host.service('prometheus')
    assert s.is_running
    assert s.is_enabled


def test_prometheus_webserver(host):

    host.socket("tcp://127.0.0.1:9090").is_listening
