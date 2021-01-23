#!/usr/bin/env python3
import sys
import os
from config import CONFIG
import datetime
import nmap3
import json
nmap = nmap3.Nmap()

class NetApi():
    def __init__(self):
        pass
    
    def getData(self):
        nmap_scan = nmap.nmap_list_scan(CONFIG["network"], arg="-sn")
        net_data=list()

        if nmap_scan["runtime"]["exit"]=="success":
            for ip in nmap_scan:
                if ip != "stats" and ip!="runtime":
                    device = dict()
                    device["ip"] = ip
                    try:
                        device["device_name"] = nmap_scan[ip]["hostname"][0]["name"].replace(CONFIG["hostname_replace"],"")
                    except:
                        device["device_name"] = None
                    net_data += [device]
            return net_data
        else:
            raise Exception(nmap_scan["runtime"])
