from netmiko import ConnectHandler
import getpass

passwd = getpass.getpass('Please enter the password: ') # Reads the output from the user and save it as a string

cisco_01 = {
    "device_type": "cisco_nxos",
    "host": "10.10.10.10",
    "username": "cisco",
    "password": passwd, # Log in password from getpass
}

connection = ConnectHandler(**cisco_01)
connection.enable() # Go to Priv EXEC mode

output = connection.send_command('show run')
print(output)

connection.disconnect()
