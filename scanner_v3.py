import socket

def port_scanner(ip, ports):
    """
    Scan a list of ports on a given IP address.

    Args:
        ip (str): The IP address to scan.
        ports (list): A list of port numbers to scan.

    Returns:
        dict: A dictionary where the keys are port numbers and the values are service names.
    """
    results = {}
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((ip, port))
            service_name = get_service_name(port)
            results[port] = service_name
            sock.close()
        except socket.error:
            results[port] = "Closed"
    return results

def get_service_name(port):
    """
    Map a port number to a service name.

    Args:
        port (int): The port number to map.

    Returns:
        str: The service name associated with the port number, or "Unknown" if not found.
    """
    # This function maps port numbers to service names
    # For simplicity, we'll use a dictionary
    service_names = {
        22: "SSH",
        80: "HTTP",
        443: "HTTPS",
        5432: "PostgreSQL",
        3306: "MySQL",
        3389: "RDP",
        21: "FTP",
        110: "POP3",
        25: "SMTP",
        143: "IMAP",
        8080: "HTTP Alternative"
    }
    return service_names.get(port, "Unknown")

def main():
    # Define the list of common ports
    common_ports = list(range(1,10000))

    # Get the IP address to scan from the user
    ip = input("Enter the IP address to scan: ")

    # Scan the ports and print the results
    results = port_scanner(ip, common_ports)

    print("Port Scan Results:")
    print("--------------------")
    for port, service in results.items():
        if service != "Closed":
            print(f"Port {port}: Open - {service}")
        else:
            print(f"Port {port}: {service}")

if __name__ == "__main__":
    main()
