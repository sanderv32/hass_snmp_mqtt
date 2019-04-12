# MAC Address tracker for Home Assistant

This tool tracks MAC addresses from a state file and publish them to a MQTT broker is a device is home or not.
At the moment it relies on the output of `snmpwalk` which is piped to this tool.


#### Example
```shell
/usr/bin/snmpbulkwalk -On -v 2c -c public 172.16.0.2 .1.3.6.1.2.1.17.4.3.1.2 | mac_to_mqtt.py --mqtt-host 172.16.0.1 --state-file /root/mac_to_mqtt.json
```