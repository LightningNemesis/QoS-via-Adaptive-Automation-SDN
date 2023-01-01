from socket import timeout
from pygnmi.client import gNMIclient
import json, threading
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

# Variables
fm151 = "10.85.128.148"  # s1
cz151 = "10.85.128.133"  # s2
do552 = "10.85.128.131"  # s3
ats330 = "10.85.128.75"  # s4
cz150 = "10.85.128.132"  # s5


switches = {
    fm151: [(2, 6), (3, 4)],
    cz151: [(1, 2), (5, 4)],
    do552: [(1, 2), (4, 3)],
    ats330: [(3, 4), (5, 1)],
    cz150: [(4, 3), (2, 4)],
}

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

R = np.matrix(np.zeros(shape=(5, 5)))


def apiCall(_host, _path, ne_sw):
    with gNMIclient(
        target=(_host, "6030"), username="admin", password="admin", insecure=True
    ) as gc:
        result = gc.get(path=[_path])

    out_uni = float(
        result["notification"][0]["update"][0]["val"][
            "openconfig-interfaces:out-unicast-pkts"
        ]
    )
    out_disc = float(
        result["notification"][0]["update"][0]["val"][
            "openconfig-interfaces:out-discards"
        ]
    )
    print(json.dumps(result, indent=4))
    if out_uni != 0:
        R[list(switches).index(_host), ne_sw - 1] = out_disc / out_uni
    else:
        R[list(switches).index(_host), ne_sw - 1] = 0


# Body
if __name__ == "__main__":
    # print(R)

    threads = []
    for key in switches:
        for ne_sw, out_port in switches[key]:
            counters_path = (
                f"interfaces/interface[name=Ethernet{out_port}]/state/counters"
            )
            t = threading.Thread(target=apiCall, args=(key, counters_path, ne_sw))
            threads.append(t)
            print(key, out_port)

    [t.start() for t in threads]
    [t.join(1000) for t in threads]
    print(R)


# iperf -c 30.0.0.1 -u -B 30.0.0.2 -b 10000m -T 60 -t 6000 -p 60500 -i 1
