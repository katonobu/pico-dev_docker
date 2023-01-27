import netifaces

def get_ipaddress_from_interface_uid(uid):
    ret_val = None
    interfaces = netifaces.interfaces()
    if uid in interfaces:
        idx = interfaces.index(uid)
        intf = interfaces[idx]
        ifaddrses = netifaces.ifaddresses(intf)
        if 2 in ifaddrses and 0 < len(ifaddrses[2]) and 'addr' in ifaddrses[2][0]:
            ret_val = ifaddrses[2][0]['addr']
    return ret_val

def get_interface_uids():
    return netifaces.interfaces()

#print(get_ipaddress_from_interface_uid('{807888C9-7BD5-4966-B923-0CAE7908D1A7}'))

if __name__ == '__main__':
    interfaces = get_interface_uids()
    for intf in interfaces:
        ip_address = get_ipaddress_from_interface_uid(intf)
        print("{} : {}".format(intf, ip_address if ip_address is not None else "N.A."))