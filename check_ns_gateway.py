#!/usr/bin/env python
# 
# Checks Netscaler gateway vserver status
# (c) 2015 Pekka Panula / Sofor Oy
# Licence: GPLv2 or later
# Version: 1.0
# Dated: 4.9.2015
# Tested on CentOS 6.x, Python v2.6.6
#
# Requirements: Citrix nitro-python api installed, download it from inside Netscaler appliance
# located: /var/netscaler/nitro/nitro-python.tgz
# unpack and install it: python setup.py install
#
# possible states:
#  "UP"
#  "DOWN"
#  "UNKNOWN"
#  "BUSY"
#  "OUT OF SERVICE"
#  "GOING OUT OF SERVICE"
#  "DOWN WHEN GOING OUT OF SERVICE"
#  "NS_EMPTY_STR"
#  "Unknown"
#  "DISABLED"
#
# nagios command template:
#  - set user macros USER47 and USER48 in resource.cfg, as username and password for Netscaler
#
# define command {
#        command_name    check_netscaler_gateway
#        command_line    $USER1$/check_ns_gateway.py --host $HOSTADDRESS$ --user '$USER47$' --password '$USER48$' --gatewayname $ARG1$ 
# }
#

import sys
import time
import sys
import argparse
from pprint import pprint

# Citrix's Nitro API
from nssrc.com.citrix.netscaler.nitro.exception.nitro_exception import nitro_exception
from nssrc.com.citrix.netscaler.nitro.service.nitro_service import nitro_service
from nssrc.com.citrix.netscaler.nitro.resource.config.vpn.vpnvserver import vpnvserver

def print_r(the_object):
    pprint(vars(the_object))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Check Netscaler gateway vserver status')
	parser.add_argument('--host', metavar='HOSTNAME', required=True, help='Netscaler hostname')
	parser.add_argument('--user', metavar='USERNAME', default='nsroot', help='Netscaler username')
	parser.add_argument('--password', metavar='PASSWORD', default='nsroot', help='Netscaler password')
	parser.add_argument('--gatewayname', metavar='GATEWAY', required=True, help='Name of Gateway vserver; Use ALL to get a list of all gateway vservers')
	
	args = parser.parse_args()

	try:
                client = nitro_service(args.host,"http")
                client.set_credential(args.user,args.password)
                client.timeout = 900

		if args.gatewayname == "ALL":
                        gwList = vpnvserver().get(client)
                        for i in range(len(gwList)):
                                print "%s: %s" % (gwList[i].name, gwList[i]._curstate)

                        client.logout()
			sys.exit(0)

		gw = vpnvserver().get(client,args.gatewayname)
		if (gw._curstate != "UP"):
			print "CRITICAL - " + gw.name + " state: " + gw._curstate
			print_r(gw)
			client.logout()
			sys.exit(2)	
		elif (gw._curstate == "UP"):
			print "OK - " + gw.name + " state: UP | totalusers=" +gw._curtotalusers
			print_r(gw)
			client.logout()
			sys.exit(0)	

        except nitro_exception as e:  # Error Handling
            print("Error - " + e.message)
            sys.exit(3)
        except Exception as e:
            print("Error - " + str(e.args))
            sys.exit(3)

