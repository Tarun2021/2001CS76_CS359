from scapy.all import *
def dns_packet_capture():
    dns_server = "8.8.8.8"
    domain = "www.bestbuy.com"
    
    dns_query_packet = IP(dst=dns_server)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=domain))
    
    
    response_packet=sr1(dns_query_packet,verbose=0)
    print(response_packet.summary())
    packets = PcapWriter("./DNS_request_response_2001cs76.pcap")
    packets.write(dns_query_packet)
    packets.write(response_packet)

def icmp_packet_capture():
    ping_request=IP(dst="www.bestbuy.com")/ICMP()
    response=sr1(ping_request,verbose=0)
    print(response.summary())
    file=PcapWriter("./PING_request_response__2001CS76.pcap")
    file.write(ping_request)
    file.write(response)
def arp_packet_capture():
    capture=sniff(filter="arp",count=2)
    wrpcap("ARP_request_response_2001CS76.pcap",capture)

def tcp_3_way_handshake():
    randsport = random.randint(1024,65535)
    syn_packet= IP(dst='www.bestbuy.com') / TCP(sport=randsport,dport=80,seq=1000)
    synack_packet= sr1(syn_packet)
    ack_packet= IP(dst='www.bestbuy.com') / TCP(sport=randsport, dport=80, flags='A', seq=synack_packet.ack, ack=synack_packet.seq + 1)
    print(syn_packet.summary())
    print(synack_packet.summary())
    print(ack_packet.summary())
    file=PcapWriter("./TCP_3_way_handshake_start_2001CS76.pcap")
    file.write(syn_packet)
    file.write(synack_packet)
    file.write(ack_packet)


arp_packet_capture()
dns_packet_capture()
tcp_3_way_handshake()
icmp_packet_capture()    