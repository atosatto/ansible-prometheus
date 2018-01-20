Ansible Role: Prometheus
========================

Install and configure Prometheus.

Requirements
------------

An Ansible 2.2 or higher installation.

Role Variables
--------------

Available variables are listed below, along with default values (see defaults/main.yml):

    prometheus_release_tag: "latest"

The Prometheus release to be installed.
By default, the latest release published at https://github.com/prometheus/prometheus/releases.

    prometheus_user: "prometheus"
    prometheus_group: "prometheus"

Prometheus system user and group.

    prometheus_install_path: "/opt"

Directory containing the downloaded Prometheus release artifacts.

    prometheus_bin_path: "/usr/local/bin"

Directory to which the Prometheus binaries will be symlinked.

    prometheus_config_path: "/etc/prometheus"
    prometheus_config_file: "prometheus.yml"

Prometheus configuration file and directory

    prometheus_config: {}

YAML dictionary holding the Prometheus configuration.
The complete Prometheus configuration reference can be found at
https://prometheus.io/docs/prometheus/latest/configuration/configuration/.<br/>
**NOTE**: the provided prometheus configuration will be merged with the default one defined in `vars/main.yml`.

    prometheus_listen_address: "127.0.0.1:9090"

The Prometheus WebServer listen ip address and port.<br/>
**NOTE**: the Prometheus metrics will be available at `{{ prometheus_listen_address }}/metrics`.

    prometheus_tsdb_path: "/var/lib/prometheus"
    prometheus_tsdb_retention: "15d"

Directory containing the Prometheus time-series database files.
By default, the old data will be deleted after 14 days.
An in depth analysis of the Operational Aspects of Prometheus Storage is available at 
https://prometheus.io/docs/prometheus/latest/storage/#operational-aspects.

    prometheus_log_level: "info"

Prometheus deamon log verbosity level.

    prometheus_additional_cli_args: ""

Additional command-line arguments to be added to the Prometheus service unit.
For the complete refence of the available CLI arguments please refer to the output
of the `prometheus --help` command.

Dependencies
------------

None.

Example Playbook
----------------

    $ cat playbook.yml
    - name: "Install and configure Prometheus"
      hosts: all
      roles:
        - { role: atosatto.prometheus }

Testing
-------

Tests are performed by [Molecule](http://molecule.readthedocs.org/en/latest/).

    $ pip install tox

To test all the scenarios run

    $ tox

To run a custom molecule command

    $ tox -e py27-ansible23 -- molecule test -s prometheus-latest 

License
-------

MIT

Author Information
------------------

Andrea Tosatto ([@\_hilbert\_](https://twitter.com/_hilbert_))
