# routeros-collectd

Python Collectd plugin for RouterOS/MikroTik using the Python [librouteros](https://pypi.org/project/librouteros/) and [collectd-python](https://collectd.org/documentation/manpages/collectd-python.5.shtml).

This plugin collects cpu-load, free-memory (from `/system resource monitor`), and tx & rx bytecount for any interface under `/interface`.

# collectd.conf

Example configuration:

```apache
LoadPlugin python
<Plugin python>
    ModulePath "/path/to/routeros-collectd"
    Import "routeros"
    <Module routeros>
        Host "127.0.0.1"
        User "username"
        Password "password"
        Interface "ether10"
    </Module>
</Plugin>
```
