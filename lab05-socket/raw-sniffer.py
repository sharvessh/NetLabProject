import socket

# SOCK_RAW = we get the raw IP packet, header included
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
print('Sniffing ICMP packets... (Ctrl+C to stop)')

while True:
    packet, addr = sock.recvfrom(65535)

    header_len = (packet[0] & 0x0F) * 4       # IP header length in bytes
    ttl        = packet[8]
    src_ip     = socket.inet_ntoa(packet[12:16])
    dst_ip     = socket.inet_ntoa(packet[16:20])
    icmp_type  = packet[header_len]           # first byte after the IP header

    if icmp_type == 8:
        kind = 'Echo Request (ping)'
    elif icmp_type == 0:
        kind = 'Echo Reply (pong)'
    else:
        kind = 'Other (type %d)' % icmp_type

    print(src_ip, '->', dst_ip, '| TTL:', ttl, '|', kind, '| size:', len(packet))