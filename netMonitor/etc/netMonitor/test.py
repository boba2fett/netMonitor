#!/usr/bin/env python3
import nmap3
import json
nmap = nmap3.Nmap()

nmap_scan = nmap.nmap_list_scan("192.168.178.0/24", arg="-sn")
#print(json.dumps(nmap_scan,indent=3))

net_data=list()

if nmap_scan["runtime"]["exit"]=="success":
    for ip in nmap_scan:
        if ip != "stats" and ip!="runtime":
            device = dict()
            device["ip"] = ip
            try:
                device["device_name"] = nmap_scan[ip]["hostname"][0]["name"]
            except:
                device["device_name"] = None
            #print(f"{ip} {hostname}")
            net_data += [device]
    print(json.dumps(net_data,indent=3))
else:
    Exception(nmap_scan["runtime"])