import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_prometheus_custom_config(host):

    f = host.file('/etc/prometheus/prometheus.yml')

    # we check that the scrape_interval variables is now set to 1m
    assert f.contains('scrape_interval: 1m')
    # we check that the evaluation_interval is left to 15s as defined in vars/main.yml
    assert f.contains('evaluation_interval: 15s')
    # we check that the new variable called 'scrape_timeout' as been added to the global configuration
    assert f.contains('scrape_timeout: 10s')
    # we check that the 'prometheus' job is defined
    assert f.contains('job_name: prometheus')
    # we check that the 'node_exporter' job is defined
    assert f.contains('job_name: node_exporter')


def validate_prometheus_config(host):

    host.run_test("/usr/local/bin/promtool check config /etc/prometheus/prometheus.yml")


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
    assert oct(f.mode) == '0644'

    host.run_test("/usr/local/bin/promtool check config /etc/prometheus/prometheus.yml")
