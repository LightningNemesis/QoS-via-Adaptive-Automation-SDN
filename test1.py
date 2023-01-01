from pygnmi.client import gNMIclient, telemetryParser
import json

fm151 = ("10.85.128.148", "6030")
do552 = ("10.85.128.131", "6030")
ats330 = ("10.85.128.75", "6030")
cz151 = ("10.85.128.133", "6030")
cz150 = ("10.85.128.132", "6030")

# host = ("10.81.108.100", "6030")
host = cz150

subscribe = {
    "subscription": [
        {
            "path": "interfaces/interface[name=Ethernet1]/state/counters",
            "mode": "sample",
            "sample_interval": 5000000000,
        },
    ],
    "mode": "stream",
    "encoding": "json",
}


with gNMIclient(target=host, username="admin", password="admin", insecure=True) as gc:

    telemetry_stream = gc.subscribe(subscribe=subscribe)

    for telemetry_entry in telemetry_stream:
        print(telemetryParser(telemetry_entry))
