from netmiko import ConnectHandler
import getpass

passwd = getpass.getpass('Please enter the password: ')

my_devices = ['10.10.1.1','10.10.1.2', '10.10.1.3', '10.10.1.4'] #Update the IP addresses
device_list = list() #create an empty to use it later

for device_ip in my_devices:
    device = {
        "device_type": "cisco_nxos",
        "host": device_ip,
        "username": "cisco",
        "password": passwd, # Log in password from getpass
    }
    device_list.append(device)

print(device_list)

config_commands = [
    'feature ospf',
    'feature interface-vlan',
    'feature lacp',
    'feature scheduler',
    'no ip domain-lookup',
    'ip name-server 1.1.1.1 use-vrf management',
    'ip name-server 2.2.2.2 use-vrf management',
    'ip name-server 8.8.4.4 use-vrf management',
    'ip name-server 8.8.8.8 use-vrf management',
    'ip domain-name example.com',
    'no ip source-route',
    'ntp server 129.6.15.29 use-vrf default',
    'ntp server 132.163.97.1 use-vrf default',
    'ntp source-interface mgmt0',
    'snmp-server community asdfghjkl group network-operator',
    'ip access-list VTY_Access', 
    '10 permit ip 10.0.0.0 0.255.255.255 any',
    '20 permit ip 1.1.1.1/32 any',
    '30 permit ip 2.2.2.2/32 any',
    '40 permit ip 3.3.3.0/30 any',
    '50 permit ip 4.4.4.4/30 any',
    'exit',
    'snmp-server contact emailaddress.com',
    'snmp-server location "Dallas"',
    'snmp-server source-interface traps mgmt0',
    'snmp-server host 1.1.1.1 traps version 1 asdfghjkl',
    'snmp-server host 2.2.2.2 traps version 1 asdfghjkl',
    'snmp-server enable traps aaa server-state-change',
    'snmp-server enable traps feature-control FeatureOpStatusChange',
    'snmp-server enable traps sysmgr cseFailSwCoreNotifyExtended',
    'snmp-server enable traps config ccmCLIRunningConfigChanged',
    'snmp-server enable traps snmp authentication',
    'snmp-server enable traps link cisco-xcvr-mon-status-chg',
    'snmp-server enable traps bridge newroot',
    'snmp-server enable traps bridge topologychange',
    'snmp-server enable traps stpx inconsistency',
    'snmp-server enable traps stpx root-inconsistency',
    'snmp-server enable traps stpx loop-inconsistency',
    'snmp-server enable traps system Clock-change-notification',
    'snmp-server enable traps feature-control ciscoFeatOpStatusChange',
    'snmp-server enable traps syslog message-generated',
    'snmp-server community ResoundCore1104 group network-operator',
    'snmp-server community yes group network-operator',
    'ntp server 132.163.97.1 use-vrf default',
    'ntp source-interface mgmt0',
    'system login block-for 120 attempts 5 within 120',
    'ssh login-attempts 3',
    'no feature telnet',
    'password strength-check',
    'clock timezone CST -6 0',
    'clock summer-time CDT 2 Sun Mar 02:00 1 Sun Nov 02:00 60',
    'scheduler logfile size 16',
    'errdisable recovery cause link-flap',
    'logging server 1.1.1.1 4 port 5544',
    'logging source-interface mgmt0',
    'no logging monitor',
    'logging level authpri 5',
    'line vty',
    'exec-timeout 15',
    'session-limit 10',
    'access-class ACL_NAME in',
    'exit',
    'scheduler job name backup-weekly',
    'copy running-config startup-config',
    'exit',
    'scheduler schedule name sch-backup-weekly',
    'job name backup-weekly',
    'time weekly Sun:23:59',
    'exit'
    ]


for each_device in device_list:
    connection = ConnectHandler(**each_device)
    connection.enable()
    print(f'Connecting to {each_device["host"]}')
    output = connection.send_config_set(config_commands)
    print(output)

    print(f'Closing Connection on {each_device["host"]}')
    connection.disconnect()
