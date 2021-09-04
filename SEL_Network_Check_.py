from netmiko import ConnectHandler
from re import search
import json
import os

templates = "C:\\Users\\Erdem\\PycharmProjects\\NETWORK\\venv\\Scripts\\templates\\"
os.environ['NET_TEXTFSM']= templates
cpu_max = 20

cut_string_array = [];
last_string_array = [];

#eq = "router_1"
#eq = "firewall_1"
eq = "switch_1"

eq_nm = "cisco_ios"
#eq_nm = "cisco_asa"
#eq_nm = "fortinet"

for i in os.listdir(templates):
    if search(eq_nm, i):
        cut_string = i.split(eq_nm + "_")
        cut_string_array.append(cut_string[1])

#print(cut_string_array)

for i in cut_string_array:
    last_string = i.split('.textfsm')
    last_string_array.append(last_string[0])


for i in last_string_array:
    last_string_array[last_string_array.index(i)] = i.replace("_", " ")

#print(last_string_array)

numberOfDevice = 10   #sistemdeki cihaz sayısı
numberOFMeasurement= 32   #her cihaz için ölçüm yapılacak birim sayısı
blank = "          "

a, b = numberOFMeasurement, numberOfDevice

router_1 = {
    'device_type': 'cisco_ios',
    'ip': '10.51.1.2',
    'username': 'R1220',
    'password': 'Ta14551748',
    'secret': 'Ta14551748',
    'port': 22
}


# %%%%%%%%%%%%%%%%%%%%%%%%% YSHA Router 1 Connection Check %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
try:
    connection_router_1 = ConnectHandler(**router_1)
    print('Connection OK')
except Exception as e:
    print("Connection FAIL")


for i in last_string_array:
    try:
        print(i)
        if i!= "show interface transceiver":
            output = connection_router_1.send_command(i, use_textfsm=True)
        print(output)
        with open("TextFSM_Output.txt","a") as file_name:
            file_name.write("KOMUT: "+ i + "\n")
            file_name.write(json.dumps(output, indent=2) + "\n")
    except Exception as e:
        print(e)
        with open("TextFSM_Output.txt","a") as file_name:
            file_name.write("KOMUT OLMADI : " + i + "\n")
            file_name.write("KOMUT OLMADI : " + i + "\n")
    with open("TextFSM_Output.txt", "a") as file_name:
        file_name.write("-----------------------------------------------------------" + "\n")
        file_name.write("-----------------------------------------------------------" + "\n")
