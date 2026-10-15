import ipaddress as ip
import math

if __name__ == '__main__':
    print("====== SUBNET CALCULATOR TOOL =======")

    not_exit = True
    while not_exit:
        # Step 1: Input IPv4 and validate prefix
        while True:
            user_input = input("\nEnter IPv4 address and prefix (e.g., 192.168.10.0/24 or 192.168.1.50/20): \n").strip()
            try:
                # strict=False allows passing host IPs and automatically finding network boundary
                parent_net = ip.IPv4Network(user_input, strict=False)

                if parent_net.prefixlen < 16:
                    print("[!] Prefix length must be /16 or higher. Please try again.")
                    continue

                break
            except ValueError as e:
                print("[!] Invalid IPv4 or CIDR format:", e, ". Please try again.")

        # Step 2: Display parent network details
        print("\n" + "=" * 60)
        print(" NETWORK INFORMATION:", parent_net)
        print("=" * 60)
        print("Network Address   :", parent_net.network_address)
        print("Subnet Mask       :", parent_net.netmask)
        print("Broadcast Address :", parent_net.broadcast_address)

        if parent_net.prefixlen == 32:
            print("Available Host IPs:", parent_net.network_address, "(Single Host)")
            print("Total Hosts       : 1")
        elif parent_net.prefixlen == 31:
            print("Available Host IPs:", str(parent_net.network_address) + " - " + str(parent_net.broadcast_address),
                  "(RFC 3021)")
            print("Total Hosts       : 2")
        else:
            first_ip = parent_net.network_address + 1
            last_ip = parent_net.broadcast_address - 1
            print("Available Host IPs:", str(first_ip) + " - " + str(last_ip))
            print("Total Usable Hosts:", f"{parent_net.num_addresses - 2:,}")

        # Step 3: Prompt for number of subnets
        max_borrowable_bits = 32 - parent_net.prefixlen
        num_subnets = None
        new_prefix = None

        if max_borrowable_bits <= 0:
            print("\n[!] This /32 network cannot be subnetted further.")
        else:
            max_possible_subnets = 2 ** max_borrowable_bits

            while True:
                try:
                    prompt = "\nEnter desired number of subnets (Power of 2, e.g., 2, 4, 8... up to " + str(
                        max_possible_subnets) + "): "
                    requested_count = int(input(prompt).strip())

                    if requested_count <= 1:
                        print("[!] Number of subnets must be greater than 1.")
                        continue
                    if requested_count > max_possible_subnets:
                        print("[!] Cannot create", requested_count,
                              "subnets. Maximum possible is " + str(max_possible_subnets) + ".")
                        continue

                    subnet_bits = math.ceil(math.log2(requested_count))
                    num_subnets = 2 ** subnet_bits
                    new_prefix = parent_net.prefixlen + subnet_bits

                    if num_subnets != requested_count:
                        print("[*] Subnets are created in powers of 2. Rounding up to", num_subnets,
                              "subnets (/" + str(new_prefix) + ").")

                    break
                except ValueError:
                    print("[!] Please enter a valid integer.")

        # Step 4: Display created subnets
        if num_subnets and new_prefix:
            subnets = list(parent_net.subnets(new_prefix=new_prefix))

            print("\n" + "=" * 85)
            print(" CREATED", len(subnets), "SUBNETS (Prefix: /" + str(new_prefix) + " | Subnet Mask:",
                  str(subnets[0].netmask) + ")")
            print("=" * 85)
            print(f"{'Subnet #':<10} | {'Network Address':<18} | {'Usable Host Range':<31} | {'Broadcast Address'}")
            print("-" * 85)

            max_display = 256
            for idx, sub in enumerate(subnets, start=1):
                if idx > max_display:
                    print("\n[Note] Output capped at", max_display,
                          "subnets to prevent terminal lag (" + f"{num_subnets - max_display:,}" + " additional subnets created).")
                    break

                if sub.prefixlen == 32:
                    usable_range = str(sub.network_address) + " (Single Host)"
                elif sub.prefixlen == 31:
                    usable_range = str(sub.network_address) + " - " + str(sub.broadcast_address)
                else:
                    usable_range = str(sub.network_address + 1) + " - " + str(sub.broadcast_address - 1)

                print(f"{idx:<10} | {str(sub.network_address):<18} | {usable_range:<31} | {sub.broadcast_address}")

        # Prompt to continue or exit
        choice = input("\nWould you like to analyze another network? (y/n): ").strip().lower()
        if choice != 'y':
            print("\nExiting .... Goodbye!")
            not_exit = False