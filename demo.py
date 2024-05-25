import socket

# Addresses to scan
ip = "192.168.0.186"

# Ports to scan
ports = [22, 80, 443, 3389]

# Iterate through ports
for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((ip, port))
    if result == 0:
        print("Port {} is open".format(port))
    else:
        print("Port {} is closed".format(port))
    sock.close()