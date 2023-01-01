from pygnmi.client import gNMIclient, telemetryParser
import json


fm151 = ('110.85.128.148', '6030')

do552 = ('10.85.128.131', '6030')
ats330 = ('10.85.128.75', '6030')
cz151 = ('10.85.128.133', '6030')
cz150 = ('10.85.128.132', '6030')

subscribe = {
    "subscription": [
        {
            "path": "interfaces/interface[name=Ethernet1]/state/counters",
            "mode": "sample",
            "sample_interval": 10000000000,
        },

    ],
    "mode": "stream",
    "encoding": "json",
}


with gNMIclient(target=fm151, username='eapiuser', password='arastra', insecure=True) as gc:

    telemetry_stream = gc.subscribe(subscribe=subscribe)

    for telemetry_entry in telemetry_stream:
        print(telemetry_entry)
