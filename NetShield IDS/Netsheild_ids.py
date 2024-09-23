import os
import subprocess
from scapy.all import sniff
from scapy.layers.inet import IP, ICMP

# Function to log detected ICMP packets
def log_packet(packet):
    ip_src = packet[IP].src
    ip_dst = packet[IP].dst
    print(f"[ALERT] ICMP Packet detected! Source: {ip_src}, Destination: {ip_dst}")
    
    # Block the IP address using iptables
    block_ip(ip_src)
    
    # Log to file
    with open("intrusion_log.txt", "a") as log_file:
        log_file.write(f"ICMP Packet: Source: {ip_src}, Destination: {ip_dst}\n")

# Function to block IP using iptables
def block_ip(ip):
    print(f"[FIREWALL] Blocking IP: {ip}")
    subprocess.call(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])

# Start the Snort IDS and monitor for ICMP traffic
def start_snort():
    print("[INFO] Starting Snort IDS...")
    subprocess.Popen(["sudo", "snort", "-A", "fast", "-i", "eth0", "-c", "/etc/snort/snort.conf"])

# Sniff packets and detect ICMP
def detect_icmp():
    print("[INFO] Starting packet sniffing for ICMP traffic...")
    sniff(filter="icmp", prn=log_packet, store=0)

if __name__ == "__main__":
    # Start snort in the background
    start_snort()
    
    # Start detecting ICMP traffic
    detect_icmp()
