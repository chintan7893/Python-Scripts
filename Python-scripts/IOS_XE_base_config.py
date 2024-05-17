from netmiko import ConnectHandler
import getpass

passwd = getpass.getpass('Please enter the password: ')

my_devices = ['10.20.20.20','10.10.10.10'] #Update the IP addresses
device_list = list() #create an empty list to use it later

for device_ip in my_devices:
    device = {
        "device_type": "cisco_xe",
        "host": device_ip,
        "username": "cisco", # Username
        "password": passwd, # Log in password from getpass
    }
    device_list.append(device)

print(device_list)

config_commands = [
    'no ip bootp server',
    'no service dhcp',
    'logging trap informational',
    'no platform punt-keepalive disable-kernel-core',
    'no logging console',
    'clock timezone CST -6 0',
    'clock summer-time CDT recurring',
    'no subscriber templating',
    'no ip domain lookup',
    'ip domain name resoundnetworks.com',
    'login block-for 600 attempts 3 within 600',
    'login quiet-mode access-class 100',
    'login on-failure log',
    'no ip forward-protocol nd',
    'ip tftp source-interface GigabitEthernet0',
    'ip ssh bulk-mode 131072',
    'no ip http server',
    'no ip http secure-server',
    'no ip http authentication local',
    'ip nat translation timeout 3600',
    'ip nat translation tcp-timeout 3600',
    'ip nat translation udp-timeout 60',
    'ip nat translation max-entries 2147483647',
    'ip scp server enable',
    'ip route vrf Mgmt-intf 0.0.0.0 0.0.0.0 10.10.10.1 200',
    'line aux 0',
    'transport input none',
    'line vty 0 4',
    'access-class 100 in vrf-also',
    'exec-timeout 15 0',
    'exit',
    'logging source-interface GigabitEthernet0 vrf Mgmt-intf',
    'logging host 1.1.1.1 transport udp port 5544',
    'ip access-list extended 100',
    '10 permit ip 20.20.20.0 0.255.255.255 any',
    '20 permit ip 10.10.10.0 0.0.0.255 any',
    'exit',
    'snmp-server community ResoundCore1104 RO',
    'snmp-server trap-source GigabitEthernet0',
    'snmp-server location "Dallas"',
    'snmp-server contact example.com',
    'snmp-server enable traps snmp authentication linkdown linkup coldstart warmstart',
    'snmp-server enable traps ospf state-change',
    'snmp-server enable traps ospf errors',
    'snmp-server enable traps ospf retransmit',
    'snmp-server enable traps ospf lsa',
    'snmp-server enable traps ospf cisco-specific errors',
    'snmp-server enable traps ospf cisco-specific retransmit',
    'snmp-server enable traps ospf cisco-specific lsa',
    'snmp-server enable traps aaa_server',
    'snmp-server enable traps cef resource-failure peer-state-change peer-fib-state-change inconsistency',
    'snmp-server enable traps memory bufferpeak',
    'snmp-server enable traps fru-ctrl',
    'snmp-server enable traps entity-qfp mem-res-thresh throughput-notif',
    'snmp-server enable traps entity-sensor',
    'snmp-server enable traps entity-state',
    'snmp-server enable traps event-manager',
    'snmp-server enable traps license',
    'snmp-server enable traps bgp cbgp2',
    'snmp-server enable traps pki',
    'snmp-server enable traps flash insertion removal lowspace',
    'snmp-server enable traps config',
    'snmp-server enable traps config-ctid',
    'snmp-server enable traps entity',
    'snmp-server enable traps cpu threshold',
    'snmp-server enable traps config-copy',
    'snmp-server enable traps syslog',
    'snmp-server enable traps auth-framework sec-violation',
    'snmp-server enable traps ipsla',
    'snmp-server enable traps entity-diag boot-up-fail hm-test-recover hm-thresh-reached scheduled-test-fail',
    'snmp-server enable traps smart-license',
    'snmp-server enable traps alarms informational',
    'snmp-server enable traps vrfmib vrf-up vrf-down vnet-trunk-up vnet-trunk-down',
    'snmp-server enable traps transceiver all',
    'snmp-server host 10.10.10.10 xyz',
    'snmp-server host 20.20.20.20 xyz',
    'ntp source GigabitEthernet0',
    'ntp server 132.163.97.1',
    'ntp server 129.6.15.28',
    'license boot level network-advantage',
]

for each_device in device_list:
    connection = ConnectHandler(**each_device)
    connection.enable()
    print(f'Connecting to {each_device["host"]}')
    output = connection.send_config_set(config_commands)
    print(output)

    print(f'Closing Connection on {each_device["host"]}')
    connection.disconnect()
