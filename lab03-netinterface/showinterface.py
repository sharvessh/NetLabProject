import netifaces

# Get all the network interfaces on the host
ifaces = netifaces.interfaces()
for ifa in ifaces:  # for each interface
    print("Network interface: ", ifa)    # display the interface name
    addrs = netifaces.ifaddresses(ifa)  # get all addresses on all interfaces

    # delete unnecessary information of AF_LINK on loopback interface
    # the key in addrs for loopback is addrs[netifaces.AF_LINK]
    if ifa == 'lo':
        del addrs[netifaces.AF_LINK]

    for family, addresses in addrs.items():  # for each address family in the addrs
        # Capture and display the current addresses within the address family
        for current_addr in addresses:
            if family == netifaces.AF_LINK:
                print("  MAC address:", current_addr.get('addr'))
            else:
                print("  IP address:", current_addr.get('addr'))

            if ifa == 'lo':  # Loopback address does not have broadcast address
                print("\t Peer:", current_addr.get('peer'))
            else:
                print("\t Broadcast address:", current_addr.get('broadcast'))

            print("\t Subnet mask:", current_addr.get('netmask'))
            # print("\n")

# Get the default gateway
print("Default gateway:", netifaces.gateways().get('default')[netifaces.AF_INET][0])