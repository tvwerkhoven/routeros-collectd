#!/usr/bin/env python3
# 
# routeros collectd plugin built on librouteros-py

import collectd
import ssl
from librouteros import connect

HOST = '127.0.0.1'		# host to connect to
HOSTNAME = 'mikrotik'   # name to use as host for collectd
USER = 'user'			# username, set in system -> users
PASSWORD = 'password'	# username, set in system -> users
INTERFACE = 'ether0'	# interface to track tx/rx for, usually used for WAN interface
API = None				# used by script to track connection to router

def config_func(config):
	for node in config.children:
		key = node.key.upper()
		val = node.values[0]

		if key == 'HOST':
			global HOST
			HOST = val
			collectd.info('routeros plugin: Using overridden HOST %s' % HOST)
		elif key == 'HOSTNAME':
			global HOSTNAME
			HOSTNAME = val
			collectd.info('routeros plugin: Using overridden HOSTNAME %s' % HOSTNAME)
		elif key == 'USER':
			global USER
			USER = val
			collectd.info('routeros plugin: Using overridden USER %s' % USER)
		elif key == 'PASSWORD':
			global PASSWORD
			PASSWORD = val
			collectd.info('routeros plugin: Using overridden PASSWORD')
		elif key == 'INTERFACE':
			global INTERFACE
			INTERFACE = val
			collectd.info('routeros plugin: Using overridden INTERFACE %s' % INTERFACE)
		else:
			collectd.info('routeros plugin: Unknown config key "%s"' % key)

def init_func():
	collectd.info('routeros plugin: init config')
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.set_ciphers('ADH:@SECLEVEL=0')
	ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
	global API
	API = connect(
		username=USER,
		password=PASSWORD,
		host=HOST,
		ssl_wrapper=ctx.wrap_socket,
		port=8729
	)

def read_func():
	# collectd.info('routeros plugin: read data')

	# First create desired path.
	interfaces = API.path('interface')
	# {'.id': '*E', 'name': 'WAN_VLAN', 'type': 'vlan', 'mtu': 1500, 'actual-mtu': 1500, 'l2mtu': 1594, 'mac-address': 'DE:AD:BE:EF:70:1C', 'last-link-down-time': 'nov/19/2021 21:12:30', 'last-link-up-time': 'nov/19/2021 21:12:53', 'link-downs': 1, 'rx-byte': 141089032, 'tx-byte': 11222723, 'rx-packet': 117721, 'tx-packet': 80098, 'rx-drop': 0, 'tx-drop': 0, 'tx-queue-drop': 0, 'rx-error': 0, 'tx-error': 0, 'fp-rx-byte': 141089032, 'fp-tx-byte': 0, 'fp-rx-packet': 117721, 'fp-tx-packet': 0, 'running': True, 'disabled': False}

	resources = API.path('system', 'resource')
	# {'uptime': '4d7h27m6s', 'version': '6.47 (stable)', 'build-time': 'Jun/02/2020 07:38:00', 'free-memory': 48701440, 'total-memory': 134217728, 'cpu': 'MIPS 74Kc V4.12', 'cpu-count': 1, 'cpu-frequency': 600, 'cpu-load': 2, 'free-hdd-space': 108892160, 'total-hdd-space': 134217728, 'write-sect-since-reboot': 311063, 'write-sect-total': 550052, 'bad-blocks': '0.1', 'architecture-name': 'mipsbe', 'board-name': 'RB2011UiAS', 'platform': 'MikroTik'}

	health = API.path('system', 'health')
	# {'voltage': 24, 'temperature': 39}

	# Dispatch values to collectd
	val = collectd.Values(host=HOSTNAME, plugin='cpu', type='percent', type_instance='active')
	# val.plugin = 'routeros'
	val.dispatch(values=[tuple(resources)[0]['cpu-load']])

	val2 = collectd.Values(host=HOSTNAME, plugin='memory', type='memory', type_instance='free')
	# val2.plugin = 'routeros'
	val2.dispatch(values=[tuple(resources)[0]['free-memory']])

	# Get INTERFACE Tx/Rx data
	for intf in interfaces:
		if (intf['name'] == INTERFACE):
			val3 = collectd.Values(host=HOSTNAME, plugin='interface', plugin_instance=INTERFACE, type='if_octets')
			val3.dispatch(values=[intf['rx-byte'],intf['tx-byte']])
			val4 = collectd.Values(host=HOSTNAME, plugin='interface', plugin_instance=INTERFACE, type='if_packets')
			val4.dispatch(values=[intf['rx-packet'],intf['tx-packet']])
			val5 = collectd.Values(host=HOSTNAME, plugin='interface', plugin_instance=INTERFACE, type='if_dropped')
			val5.dispatch(values=[intf['rx-drop'],intf['tx-drop']])
			val6 = collectd.Values(host=HOSTNAME, plugin='interface', plugin_instance=INTERFACE, type='if_errors')
			val6.dispatch(values=[intf['rx-error'],intf['tx-error']])

	val7 = collectd.Values(host=HOSTNAME, plugin='sensors', type='temperature', type_instance='cpu')
	val7.dispatch(values=[tuple(health)[0]['temperature']])


collectd.register_config(config_func)
collectd.register_init(init_func)
collectd.register_read(read_func)
