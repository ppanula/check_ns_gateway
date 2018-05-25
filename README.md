Nagios/Naemon check plugin:
Checks Netscaler gateway vserver status.

Tested on CentOS 6.x, SCL Python v2.7

Requirements: 
- SSL options requires Python 2.7+ to work correctly, this assumes that SCL Python27 is installed.
```
  yum install -y centos-release-SCL
  yum install -y python27 
```

- Citrix nitro-python api installed, download it from inside Netscaler appliance
  located: /var/netscaler/nitro/nitro-python.tgz
  unpack and install it: ```python setup.py install``` or install with SCL: ```scl enable python27 "python setup.py install"```

nagios command template:
  - set user macros USER47 and USER48 in resource.cfg, as username and password for Netscaler

```
 define command {
        command_name    check_netscaler_gateway
        command_line    $USER1$/check_ns_gateway.py --host $HOSTADDRESS$ --user '$USER47$' --password '$USER48$' --gatewayname $ARG1$ 
 }
 ```
 Templates for HTTPS with/without cert verification, using SCL Python v2.7:
 ```
 define command {
        command_name    check_netscaler_gateway_ssl
        command_line    scl enable python27 "$USER1$/check_ns_gateway.py --ssl --host $HOSTADDRESS$ --user $USER47$ --password $USER48$ --gatewayname $ARG1$ "
 }

 define command {
        command_name    check_netscaler_gateway_ssl_noverify
        command_line    scl enable python27 "$USER1$/check_ns_gateway.py --ssl --nosslverify --host $HOSTADDRESS$ --user $USER47$ --password $USER48$ --gatewayname $ARG1$ "
 }
 ```
 
