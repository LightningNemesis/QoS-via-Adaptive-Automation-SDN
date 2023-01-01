from jsonrpclib import Server
from pprint import pprint as pp

username = "admin"
password = "admin"
ip = "10.85.128.148"
url = "http://" + username + ":" + password + "@" + ip + "/command-api"
switch = Server(url)

f = open("commands.txt", "r")
conf = f.read().splitlines()
f.close()

# result = switch.runCmds(version=1, cmds=["show version"])
pp(conf)
conf_vlans = switch.runCmds(version=1, cmds=conf, autoComplete=True)
result = switch.runCmds(
    version=1, cmds=["sh policy-map"], format="json", autoComplete=True
)
