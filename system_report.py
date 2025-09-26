#!/usr/bin/python3.9

import subprocess, os, re
from datetime import datetime

# Alex Fratepietro
# credit to chatpgt for some debug questions and regex

LOG = ""
HOSTNAME = ""

def start():
    # prints the header to the program with date and system report
    global LOG
    txt = f"System Report - {datetime.today()}"
    print(f"\033[91m\t\t\t{txt}\n\033[00m")
    # add to text log
    LOG += txt+"\n"

def device_information():
    #prints device information
    global LOG,HOSTNAME
    print(f"\033[92mDevice Information\n\033[00m")
    #Hostname
    hostname = subprocess.run("hostname -f",capture_output=True,shell=True).stdout.strip().decode() # run linux command
    print(f"Hostname: \t\t\t{hostname}")
    HOSTNAME = hostname
    #Domain
    domain_name = subprocess.run("domainname",capture_output=True,shell=True).stdout.strip().decode() # run linux command
    print(f"Domain: \t\t\t{domain_name}")
    # add to text log
    LOG += f"Hostname: {hostname}, Domain: {domain_name}\n"

def network_information():
    global LOG
    print(f"\033[92mNetwork Information\n\033[00m")
    #IP address
    ifconfig = subprocess.run("ifconfig",capture_output=True,shell=True).stdout.strip().decode() # run linux command
    ip_addr = re.search(r"inet\s+(\d{1,3}(?:\.\d{1,3}){3})", ifconfig) #searches for first mention inet and gets the ip address after
    print(f"IP Address: \t\t\t{ip_addr.group(1)}")
    #Gateway
    gateway = subprocess.run("ip r",capture_output=True,shell=True).stdout.strip().decode()[12:27] # run linux command
    print(f"Gateway: \t\t\t{gateway}")
    #Net mask
    slash_value = re.search(r"netmask\s+(\d{1,3}(?:\.\d{1,3}){3})", ifconfig) #searches for first mention netmask and gets the ip address after
    print(f"Netmask: \t\t\t{slash_value.group(1)}")
    #DNS 1&2
    dns = subprocess.run("cat /etc/resolv.conf",capture_output=True,shell=True).stdout.strip().decode() # run linux command
    ips = re.findall(r"nameserver\s+(\d{1,3}(?:\.\d{1,3}){3})", dns) #searches for all dns and gets the ip address after
    print(f"DNS1: \t\t\t\t{ips[0]}")
    # add to text log
    print(f"DNS2: \t\t\t\t{ips[1]}")
    LOG += f"IP address: {ip_addr.group(1)}, gateway: {gateway}, netmask: {slash_value.group(1)}, dns1: {ips[0]}, dns2: {ips[1]}\n"

def os_information():
    global LOG
    print(f"\033[92mOperating System Information\n\033[00m")
    # OS
    os_info = subprocess.run("cat /etc/os-release",capture_output=True,shell=True).stdout.strip().decode() #Opens os-release file
    os_name = re.search(r'^PRETTY_NAME="([^"]+)"', os_info,re.MULTILINE) #searches for Pretty_name in /etc/os-release
    print(f"Operating System: \t\t\t{os_name.group(1)}")
    # OS Version
    os_version = re.search(r'^VERSION_ID="([^"]+)"', os_info,re.MULTILINE) #searches for version_id in /etc/os-release
    print(f"Operating Version: \t\t\t{os_version.group(1)}")
    # Kernal Version
    kernal = subprocess.run("uname -r",capture_output=True,shell=True).stdout.strip().decode() # gets only kernal version
    print(f"Kernal Version: \t\t\t{kernal}")
    # add to text log
    LOG += f"os: {os_name.group(1)}, os version: {os_version.group(1)}, kernal version: {kernal}\n"

def storage_info():
    global LOG
    print(f"\033[92mStorage Information\n\033[00m")
    # System Drive Total:
    info = subprocess.run("df -h", capture_output=True, text=True).stdout # gets information relating to system storage
    match = re.findall(r'(\d+(?:\.\d+)?)G', info) #gets all the values before the gigabyte (G)
    size, used, avail = match[0],match[1],match[2] #assigns them to their correct names
    print(f"Size: \t\t\t{size}GiB")
    # System Drive Used:
    print(f"Used: \t\t\t{used}GiB")
    # System Drive Free:
    print(f"Available: \t\t\t{avail}GiB")
    # add to text log
    LOG += f"Size: {size}, Used: {used}, Avail: {avail}\n"

def processor_info():
    global LOG
    print(f"\033[92mProcessor Information\n\033[00m")
    model = None
    processors = 0
    cores = set()

    with open("/proc/cpuinfo") as f: #goes through /proc/cpuinfo file to find model name processors and cores
        for line in f:
            if line.startswith("model name") and model is None:
                model = line.split(":", 1)[1].strip()
            if line.startswith("processor"):
                processors += 1
            if line.startswith("core id"):
                cores.add(line.split(":", 1)[1].strip())
    # CPU model
    print(f"CPU Model: \t\t\t{model}")
    # Number of Processors 
    print(f"Number of processors: \t\t\t{processors}")
    # Number of Cores
    print(f"Number of cores: \t\t\t{len(cores)}")
    # add to text log
    LOG += f"CPU Model: {model}, Processors: {processors}, Cores: {len(cores)}\n"
    

def memory_info():
    global LOG
    print(f"\033[92mMemory Information\n\033[00m")
    # Total RAM
    info = subprocess.run("free -h",capture_output=True,shell=True).stdout.strip().decode() #gets information relating to RAM
    match = re.findall(r'(\d+(?:\.\d+)?)Gi', info) # gets all the values before the gigabyte (Gi)
    total, avail = match[0], match[1] #assigns them to their correct names
    print(f"Used: \t\t\t{total}GiB")
    # Available RAM
    print(f"Available: \t\t\t{avail}GiB")
    # add to text log
    LOG += f"Used: {total}, Avail: {avail}\n"

def write_file():
    filename = HOSTNAME + "_system_report.log"
    with open(filename,"w")as syslog:
        syslog.write(LOG)


def main():
    start()
    device_information()
    network_information()
    os_information()
    storage_info()
    processor_info()
    memory_info()

os.system('clear')
main()