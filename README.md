# routeros-collectd

Python Collectd plugin for RouterOS/MikroTik using the Python [librouteros](https://pypi.org/project/librouteros/) and [collectd-python](https://collectd.org/documentation/manpages/collectd-python.5.shtml), superseding the abandoned [Plugin:RouterOS](https://collectd.org/wiki/index.php/Plugin:RouterOS)

This plugin collects the following parameters from a MikroTik router:
* cpu: percent active (from `/system resource monitor`)
* memory: free (from `/system resource monitor`)
* interface: if_octets, if_packets, if_errors, if_dropped (from `/interface`)

# Installation

1. Store `routeros.py` in a known location accessible by the `collectd` daemon, e.g. `/opt/collectd_plugins/`
2. Create a user on your MikroTik router with read only access via web interface under System -> Users
3. Update `collectd.conf` to configure credentials and interface to monitor (probably your WAN interface):
```apache
LoadPlugin python
<Plugin python>
    ModulePath "/opt/collectd_plugins"
    Import "routeros"
    <Module routeros>
        Host "127.0.0.1"
        User "username"
        Password "password"
        Interface "ether10"
    </Module>
</Plugin>
```
4. Restart collectd, check log file for issues: `sudo systemctl restart collectd && sudo systemctl restart collectd`

# Sources

* [Danilo Bargen on "How to Write a Collectd Plugin with Python"](https://blog.dbrgn.ch/2017/3/10/write-a-collectd-python-plugin/)
* [Collectd-python man page](https://collectd.org/documentation/manpages/collectd-python.5.shtml)