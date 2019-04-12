#!/usr/bin/env python
import json
import os
import sys
import time

import click as click
import paho.mqtt.publish as publish


class State():
    """ JSON serialization/deserialization class """
    def __init__(self, state_file="/tmp/mac_to_mqtt.json"):
        self.state_file = state_file
        self.state_json = {}

        if os.path.exists(self.state_file):
            self._fd = open(self.state_file, "r+")
            self.state_json = json.loads(self._fd.read())
            self._fd.seek(0)
        else:
            self._fd = open(self.state_file, "w+")

    def __enter__(self):
        return self.state_json

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._fd.write(json.dumps(self.state_json))
        self._fd.truncate()
        self._fd.close()


def read_in():
    return [x.strip() for x in sys.stdin.readlines()]


@click.command()
@click.option('--mqtt-host', default='127.0.0.1', help='hostname/ip of MQTT host', show_default=True)
@click.option('--mqtt-port', default=1883, help='port number of MQTT host', show_default=True)
@click.option('--state-file', default='/tmp/mac_to_mqtt.json', help='State file location', show_default=True)
@click.option('--not-home', default=900, help='Report not home after this amount of seconds', show_default=True)
@click.option('--debug', is_flag=True, help='Only print mqtt messages')
def main(mqtt_host, mqtt_port, state_file, not_home, debug):
    mqtt_messages = []
    now = time.time()

    with State(state_file) as state:
        a = read_in()
        for b in a:
            mac_address = ":".join(format(int(x), "02x") for x in b.split(" ")[0].split(".")[13:])
            state[mac_address] = time.time()

        for mac_address, epoch in dict(state).iteritems():
            if epoch + not_home < now:
                payload = "not_home"
            else:
                payload = "home"
            mqtt_messages.append({"topic": "location/{0}".format(mac_address), "payload": payload})
    if not debug:
        publish.multiple(mqtt_messages, mqtt_host, mqtt_port)
    else:
        print mqtt_messages
    return 0


if __name__ == '__main__':
    sys.exit(main())