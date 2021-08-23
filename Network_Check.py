from netmiko import ConnectHandler
from colorama import init, Fore, Back, Style
import threading
import time
import json
import socket
from tkinter import *
import os
init
init(autoreset=True)
cpu_max = 20
"""
ilk 16 bit = Ekipman ID
son 64 bit = Ekipman Durumları
    FAIL = 1
    NORMAL = 0
    N/A (Bilgi Alınamıyor) = 9

"""
numberOfDevice = 10   #sistemdeki cihaz sayısı
numberOFMeasurement= 32   #her cihaz için ölçüm yapılacak birim sayısı
blank = "          "

a, b = numberOFMeasurement, numberOfDevice

router_1 = {
    'device_type': 'cisco_ios_telnet',
    'ip': '10.51.1.52',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco',
    'port': 23
}

router_2 = {
    'device_type': 'cisco_ios_telnet',
    'ip': '10.51.1.53',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco',
    'port': 23
}

# %%%%%%%%%%%%%%%%%%%%%%%%% YSHA Router 1 Connection Check %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
try:
    connection_router_1 = ConnectHandler(**router_1)
    print('YSHA Router 1 Telnet Connection OK')
except Exception as e:
    print("YSHA Router 1 Telnet Connection FAIL")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% YSHA Router 1 Internal Check (Power, Temperature) %%%%%%%%%%%%%%%%%%%%%%%
try:
    env = connection_router_1.send_command('show env', use_textfsm=True)
    if env == "All measured values are normal":
        print("YSHA Router 1 Internal Check PASS")
    else:
        print("YSHA Router 1 Internal FAIl (temperature or power")
except Exception as e:
    print(e)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% YSHA Router 1 CPU Check %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
try:
    cpu_router_1 = connection_router_1.send_command('show processes cpu', use_textfsm=True)
    #print(json.dumps(cpu_router_1, indent=2))
    if int(cpu_router_1[0]['cpu_1_min']) >= cpu_max:
        print('YSHA Router 1 High CPU')
    else:
        print('YSHA Router 1 Low CPU')
except Exception as e:
    print(e)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%% YSHA Router 1 Standby Status %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
try:
    standby_router_1 = connection_router_1.send_command('show standby', use_textfsm=True)
    #print(json.dumps(standby_router_1, indent=2))
    if standby_router_1[0]['state'] == 'Active':
        print('YSHA Router 1 is Active')
    elif standby_router_1[0]['state'] == 'Standby':
        print('YSHA Router 1 is Standby')
    else:
        print('Redundancy FAIL')
except Exception as e:
    print(e)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%% YSHA Router 1 Interface Status %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
try:
    router_1_interface = connection_router_1.send_command('show ip interface brief', use_textfsm=True)
    print(json.dumps(router_1_interface, indent=2))
    print("------------------------------------------------------------------------------------------------------------")
    print("{:<30} {:<30} {:<30} {:<30}".format("INTERFACE", "IP ADRESS", "STATUS", "PROTOCOL"))
    print("------------------------------------------------------------------------------------------------------------")
    for i in range(len(router_1_interface)):
        print("{:<30} {:<30} {:<30} {:<30}".format(router_1_interface[i]["intf"], router_1_interface[i]["ipaddr"], router_1_interface[i]["status"], router_1_interface[i]["proto"]))
except Exception as e:
    print(e)

router_1_interface = connection_router_1.send_command('show ip route', use_textfsm=True)
print(json.dumps(router_1_interface, indent=2))
