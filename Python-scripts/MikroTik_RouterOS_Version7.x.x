from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from netmiko import ConnectHandler
import getpass
import re

username = input('Enter your SSH username: ')
password = getpass.getpass('Please enter the password: ')

with open(r"C:\\Users\\XYZ\\ABC.txt") as f:
    devices = f.read().splitlines()
print(devices)

all_devices = []
for router in devices:
    print('Connecting to device ---> ' + router)
    ip_address = router
    mikrotik_devices = {
        'device_type': 'mikrotik_routeros',
        'ip': ip_address,
        'username': username,
        'password': password,
        'port': 22,   #Default SSH Port
    }
    all_devices.append(mikrotik_devices)

config_commands = [
    '/system identity print',
    '/system resource print',
]

name_pattern = r'name: (.+)'
version_pattern = r'Version: (\d+\.\d+)'

for device in all_devices:
    try:
        net_connect = ConnectHandler(**device)
        output = net_connect.send_config_set(config_commands) + "\n"
        
        name_match = re.search(name_pattern, output)
        device_name = name_match.group(1) if name_match else "Unknown"
        
        for line in output.split('\n'):
            if 'version' in line.lower():
                version = line.split(":")[1].strip()
                if re.match(r'^7', version):
                    print(f"Device IP: {device['ip']}, Device Name: {device_name}, Version: {version}")

        net_connect.disconnect()
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        print(f"Failed to connect to {device['ip']}: {str(e)}")
        continue
