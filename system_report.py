# add shabang later

import subprocess, os, platform, re

# credit to chatpgt for some debug questions and regex

def device_information():
    print(f"\033[92mDevice Information\n\033[00m")
    #Hostname
    hostname = subprocess.run("hostname -f",capture_output=True,shell=True).stdout.strip().decode()
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
    print(f"DNS1: \t\t\t\t{ips[0]}")
    print(f"DNS2: \t\t\t\t{ips[1]}")

def os_information():
    print(f"\033[92mOperating System Information\n\033[00m")
    # OS
    os_info = subprocess.run("cat /etc/os-release",capture_output=True,shell=True).stdout.strip().decode()
    os_name = re.search(r'^PRETTY_NAME="([^"]+)"', os_info,re.MULTILINE)
    print(f"Operating System: \t\t\t{os_name.group(1)}")
    # OS Version
    os_version = re.search(r'^VERSION_ID="([^"]+)"', os_info,re.MULTILINE)
    print(f"Operating System: \t\t\t{os_version.group(1)[:4]}")
    # Kernal Version
    kernal = subprocess.run("uname -r",capture_output=True,shell=True).stdout.strip().decode()
    print(f"Kernal Version: \t\t\t{kernal}")

def storage_info():
    print(f"\033[92mStorage Information\n\033[00m")
    # System Drive Total:
    info = subprocess.run(["df", "-h", "/"], capture_output=True, text=True).stdout
    match = re.findall(r'(\d+(?:\.\d+)?)G', info)
    size, used, avail = match[0],match[1],match[2]
    print(f"Size: \t\t\t{size}GiB")
    # System Drive Used:
    print(f"Used: \t\t\t{used}GiB")
    # System Drive Free:
    print(f"Avail: \t\t\t{avail}GiB")

def processor_info():
    print(f"\033[92mProcessor Information\n\033[00m")
    model = None
    processors = 0
    cores = set()

    with open("/proc/cpuinfo") as f:
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
    

def memory_info():
    print(f"\033[92mMemory Information\n\033[00m")
    # Total RAM
    info = subprocess.run("free -h",capture_output=True,shell=True).stdout.strip().decode()
    match = re.findall(r'(\d+(?:\.\d+)?)Gi', info)
    total, avail = match[0],match[1]
    print(f"Used: \t\t\t{total}GiB")
    # Available RAM
    print(f"Used: \t\t\t{avail}GiB")

def main():
    device_information()
    network_information()
    os_information()
    storage_info()
    processor_info()
    memory_info()

os.system('clear')
main()