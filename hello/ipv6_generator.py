import random
import ipaddress as ipaddr
from netaddr import *
# addr: an IP subnet. e.g: 2001:db8:abcd:0012::0/64
def ipv6_generator(addr):

	# generate random IPv6 with given network address
	try:
		sub_addr = IPNetwork(addr)
		randomIP_int = sub_addr.value + random.randint(0, sub_addr.size)
		randomIP = ipaddr.IPv6Address(randomIP_int)
		
		return str(randomIP)
	except:
		return 1

#ipv6_generator('2001:db8:abcd:0012::0/64')