from pygnmi.client import gNMIclient, telemetryParser
import json

host = ("10.85.128.131", "6030")

subscribe = {
    "subscription": [
        {
            "path": "eos_native:/LANZ/congestion",
            "mode": "sample",
            "sample_interval": 5000000000,
        }
    ],
    "mode": "stream",
    "encoding": "json",
}

with gNMIclient(
    target=host, username="eapiuser", password="arastra", insecure=True
) as gc:
    tele_stream = gc.subscribe(subscribe=subscribe)
    for tele_entry in tele_stream:
        data = telemetryParser(tele_entry)
        if "update" in data:
            payload = telemetryParser(tele_entry)["update"]["update"][0]
            # print(payload)
            if "qDropCount" in payload["val"]:
                print(payload["val"]["qDropCount"])
