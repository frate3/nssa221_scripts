# add shabang later
#switch hostname back to hostname -f 
#Uncomment domainname
# add correct filters to ip address and netmaks

import subprocess, os, platform, re

# credit to chatpgt for some debug questions and regex

def device_information():
    print(f"\033[92mDevice Information\n\033[00m")
    #Hostname
    # hostname = subprocess.run("hostname -f",capture_output=True,shell=True).stdout.strip().decode()
    hostname = subprocess.run("hostname",capture_output=True,shell=True).stdout.strip().decode()
    print(f"Hostname: \t\t\t{hostname}")
    #Domain
    domain_name = subprocess.run("domainname",capture_output=True,shell=True).stdout.strip().decode()
    print(f"Domain: \t\t\t{domain_name}")

def network_information():
    print(f"\033[92mNetwork Information\n\033[00m")
    #IP address
    ifconfig = subprocess.run("ifconfig",capture_output=True,shell=True).stdout.strip().decode()
    ip_addr = re.search(r"inet\s+(\d{1,3}(?:\.\d{1,3}){3})", ifconfig)
    print(f"IP Address: \t\t\t{ip_addr.group(1)}")
    #Gateway
    gateway = subprocess.run("ip r",capture_output=True,shell=True).stdout.strip().decode()[12:27]
    print(f"Gateway: \t\t\t{gateway}")
    #Net mask
    slash_value = re.search(r"netmask\s+(\d{1,3}(?:\.\d{1,3}){3})", ifconfig)
    print(f"Netmask: \t\t\t{slash_value.group(1)}")
    #DNS 1&2
    dns = subprocess.run("cat /etc/resolv.conf",capture_output=True,shell=True).stdout.strip().decode()
    ips = re.findall(r"nameserver\s+(\d{1,3}(?:\.\d{1,3}){3})", dns)
    print(f"DNS1: \t\t\t{ips[0]}")
    print(f"DNS2: \t\t\t{ips[1]}")

def os_information():
    # OS

    # OS Version

    # Kernal Version

    pass

def storage_info():
    # System Drive Total:

    # System Drive Used:

    # System Drive Free:

    pass

def processor_info():
    # CPU model

    # Number of Processors 

    # Number of Cores

    pass

def memory_info():
    # Total RAM

    # Available RAM

    pass

def main():
    # print("Hello")
    device_information()
    network_information()

os.system('clear')
main()