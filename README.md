Checks Netscaler gateway vserver status.
Tested on CentOS 6.x, Python v2.6.6

Requirements: 

Citrix nitro-python api installed, download it from inside Netscaler appliance
located: /var/netscaler/nitro/nitro-python.tgz
unpack and install it: python setup.py install

nagios command template:
  - set user macros USER47 and USER48 in resource.cfg, as username and password for Netscaler

```
 define command {
        command_name    check_netscaler_gateway
        command_line    $USER1$/check_ns_gateway.py --host $HOSTADDRESS$ --user '$USER47$' --password '$USER48$' --gatewayname $ARG1$ 
 }
 ```
 
