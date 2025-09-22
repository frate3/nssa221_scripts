#!/usr/bin/python3.9

import subprocess, re, os

# credit to chatpgt for some debug questions and regex

def start():
	#display menu and make sure input is valid
    print('''Select an option 1-5
        1. Display the default gateway
        2. Test Local Connectivity
        3. Test Remote Connectivity
        4. Test DNS Resolution
        5. Exit/quit the script
        ''')
    option = ''
    while True:
        try:
            option = int(input())
            break
        except:
            print("select a number 1-5")
    return option

def main():
    while True:
        pick = start()
        if pick==1:
			# display default gateway
        	gateway = subprocess.run("ip r",capture_output=True,shell=True).stdout.strip().decode()[12:27]
        	print(f"Default gateway is: {gateway}")
        elif pick==2:
        	#test local connectivity
        	print("starting local pings..")
        	local = subprocess.run("ping -c 5 127.0.0.1",capture_output=True,shell=True).stdout.strip().decode()
        	match = re.search(r'(\d+)\s+packets transmitted,\s+(\d+)\s+received', local)
        	if match:
        		print(match.group(0))
        elif pick == 3:
            #test outside connectivity
        	print("starting outside pings..")
        	local = subprocess.run("ping -c 5 8.8.8.8",capture_output=True,shell=True).stdout.strip().decode()
        	match = re.search(r'(\d+)\s+packets transmitted,\s+(\d+)\s+received', local)
        	if match:
        		print(match.group(0))
        elif pick == 4:
        	# Dns resolution looking up google.com on rit dns
        	dns = subprocess.run("nslookup google.com 129.21.3.17",capture_output=True,shell=True).stdout.strip().decode()
        	match = re.search(r"\*",dns)
        	if match:
        		print("DNS could not be resolved")
        	else:
        		print("DNS resolved")
        elif pick == 5:
        	print("exiting script")
        	break
        else:
        	print("invalid response")
os.system('clear')
main()
